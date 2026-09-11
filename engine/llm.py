"""Chat client for the two providers this thing can run on. Stdlib only.

Groq and Google both speak the OpenAI chat-completions shape, so one client
covers both. They differ in three ways that matter: Groq wants explicit
reasoning parameters and Google rejects them outright, Groq reports its rate
limit in response headers and Google reports nothing, and Groq returns thinking
in its own field while Gemma inlines it into the content as <thought> tags.
"""

from __future__ import annotations

import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

THOUGHT = re.compile(r"<(?:thought|think)>(.*?)</(?:thought|think)>", re.DOTALL)


@dataclass(frozen=True)
class Provider:
    url: str
    key_env: str
    default_model: str
    native_reasoning: bool
    min_interval: float
    max_output: int
    # Tokens a minute. Google sends no headers to discover this from, so it is
    # tracked locally against a rolling window instead of learned.
    tpm: int
    # Not every OpenAI-compatible provider accepts the newer parameter name.
    output_key: str = "max_completion_tokens"


PROVIDERS = {
    "groq": Provider(
        url="https://api.groq.com/openai/v1/chat/completions",
        key_env="GROQ_API_KEY",
        default_model="qwen/qwen3.8-27b",
        native_reasoning=True,
        min_interval=0.0,
        # The free tier allows 1000 output tokens a minute, so a longer answer
        # is rejected outright rather than throttled.
        max_output=900,
        # Observed from a 413: "ITPM: Limit 7000".
        tpm=7000,
    ),
    "gemini": Provider(
        url="https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        key_env="GEMINI_API_KEY",
        default_model="gemma-4-31b-it",
        native_reasoning=False,
        # No rate limit headers come back, so pace on the clock instead. The
        # free tier allows 15 requests a minute.
        min_interval=4.5,
        max_output=4000,
        # Held below the real ceiling on purpose, so the owner keeps room
        # on the same key.
        tpm=int(os.environ.get("GEMINI_TPM", "10000")),
    ),
    "zai": Provider(
        # The general API base. A Coding Plan key wants /api/coding/paas/v4
        # instead, which is a different endpoint with the same shape.
        url="https://api.z.ai/api/paas/v4/chat/completions",
        key_env="ZAI_KEY",
        default_model="glm-4.7-flash",
        # Thinking arrives inline rather than in its own field, same as Gemma.
        native_reasoning=False,
        # The documented free tier ceiling is about 60 requests a minute.
        min_interval=1.0,
        max_output=4000,
        # z.ai publishes no token per minute cap, so every number here has been
        # a guess: 60k, then 30k after run 52 was refused with 1305. 50k until
        # someone measures the real ceiling, which probe_tpm.py exists to do.
        tpm=int(os.environ.get("ZAI_TPM", "50000")),
        output_key="max_tokens",
    ),
}


class LLMError(RuntimeError):
    """Raised when the API refuses to cooperate after retries."""


def _parse_duration(raw: str) -> float:
    """Groq returns things like '2m52.8s', '472ms' or a plain seconds count."""
    raw = (raw or "").strip()
    if not raw:
        return 0.0
    if raw.endswith("ms"):
        return float(raw[:-2] or 0) / 1000
    total, number = 0.0, ""
    for char in raw:
        if char.isdigit() or char == ".":
            number += char
        elif char == "m":
            total += float(number or 0) * 60
            number = ""
        elif char == "s":
            total += float(number or 0)
            number = ""
    return total + (float(number) if number else 0.0)


@dataclass
class Usage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    # z.ai caches repeated prefixes on its own. Counted so we can tell whether
    # it is actually happening rather than assuming it from the documentation.
    cached_tokens: int = 0

    @property
    def total(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def add(self, raw: dict[str, Any] | None) -> None:
        if not raw:
            return
        self.prompt_tokens += int(raw.get("prompt_tokens", 0))
        self.completion_tokens += int(raw.get("completion_tokens", 0))
        detail = raw.get("prompt_tokens_details") or {}
        self.cached_tokens += int(detail.get("cached_tokens", 0) or 0)


@dataclass
class Client:
    api_key: str
    provider: str = "groq"
    model: str = ""
    temperature: float = 0.9
    reasoning_effort: str = "low"
    max_completion_tokens: int = 0
    max_retries: int = 10
    timeout: int = 180
    usage: Usage = field(default_factory=Usage)
    reasoning_log: list[str] = field(default_factory=list)
    # What the provider said when it refused. Kept so the journal can carry it,
    # because the Actions log is ephemeral and sealed while the run is live.
    errors: list[str] = field(default_factory=list)
    _remaining: int | None = None
    _reset_after: float = 0.0
    _last_call: float = 0.0
    _announced: bool = False
    _window: list[tuple[float, int]] = field(default_factory=list)

    @property
    def spec(self) -> Provider:
        return PROVIDERS[self.provider]

    def __post_init__(self) -> None:
        if self.provider not in PROVIDERS:
            raise LLMError(f"unknown provider {self.provider!r}")
        self.model = self.model or self.spec.default_model
        self.max_completion_tokens = self.max_completion_tokens or self.spec.max_output

    def _note_limits(self, headers) -> None:
        raw = headers.get("x-ratelimit-remaining-tokens")
        self._remaining = int(raw) if raw and raw.isdigit() else None
        self._reset_after = _parse_duration(headers.get("x-ratelimit-reset-tokens", ""))

        # Report whatever the provider is willing to tell us, once, so the run
        # log says what the real ceiling was rather than what we guessed.
        if not self._announced:
            self._announced = True
            limits = {
                key: headers.get(f"x-ratelimit-limit-{key}")
                for key in ("tokens", "requests")
            }
            found = ", ".join(f"{v} {k}" for k, v in limits.items() if v)
            print(
                f"  provider limits: {found}" if found
                else "  provider reports no rate limit headers, pacing on the clock",
                flush=True,
            )

    def _harvest_thinking(self, message: dict[str, Any]) -> None:
        """Keep the thinking for the journal, then drop it from the message.

        Replaying it into the next turn costs tokens and buys nothing.
        """
        # Providers disagree about where thinking goes. Groq calls it
        # `reasoning`, z.ai calls it `reasoning_content`, Gemma inlines it in
        # the content as tags. Check every shape rather than trusting a flag:
        # GLM-4.7 thinks whether or not it is asked to, and a whole run's worth
        # of its reasoning was being discarded unread and then resent.
        for name in ("reasoning", "reasoning_content"):
            thought = (message.pop(name, None) or "").strip()
            if thought:
                self.reasoning_log.append(thought)

        content = message.get("content") or ""
        thoughts = THOUGHT.findall(content)
        if thoughts:
            self.reasoning_log.extend(t.strip() for t in thoughts if t.strip())
            message["content"] = THOUGHT.sub("", content).strip()

    def _spent_this_minute(self) -> int:
        cutoff = time.monotonic() - 60
        self._window = [(at, n) for at, n in self._window if at > cutoff]
        return sum(n for _, n in self._window)

    def pace(self, need: int) -> None:
        """Wait out whichever limit is about to bite.

        Three of them. Requests per minute, which is a fixed gap. Tokens per
        minute, tracked here because Google reports nothing and a fast run
        blows a 16k allowance in three turns. And Groq's own token window,
        which it does report, and which is authoritative when present.
        """
        gap = time.monotonic() - self._last_call
        if self._last_call and gap < self.spec.min_interval:
            time.sleep(self.spec.min_interval - gap)

        # Keep waiting until there is actually room. Ageing out the single
        # oldest call is not always enough to make space, and stopping after
        # one sleep lets the window creep over the limit.
        # The check uses an estimate of the next prompt, but the window records
        # what was actually billed, completion included. Leave a tenth of the
        # allowance spare so that gap cannot push it over.
        ceiling = int(self.spec.tpm * 0.9)
        while self._window:
            spent = self._spent_this_minute()
            if not self._window or spent + need <= ceiling:
                break
            wait = min(60 - (time.monotonic() - self._window[0][0]) + 1, 61.0)
            if wait <= 0:
                break
            print(
                f"  pacing {wait:.0f}s: {spent:,} of {ceiling:,} usable tokens"
                f" used this minute, next call needs about {need:,}",
                flush=True,
            )
            time.sleep(wait)

        if self._remaining is not None and self._remaining < need:
            wait = min(self._reset_after + 1.0, 65.0)
            if wait > 0:
                print(f"  pacing {wait:.0f}s, {self._remaining} tokens left in window")
                time.sleep(wait)

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """One turn. Returns the assistant message dict."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "temperature": self.temperature,
            self.spec.output_key: self.max_completion_tokens,
        }
        if self.spec.native_reasoning:
            # Tool calling rejects the raw format, which would inline the
            # thinking into content as think tags.
            payload["reasoning_format"] = "parsed"
            if self.reasoning_effort:
                payload["reasoning_effort"] = self.reasoning_effort

        message = self._post(payload)
        self._harvest_thinking(message)
        return message

    def ask(self, prompt: str, max_tokens: int = 700) -> str:
        """A plain question with no tools. Paced and charged like any call.

        This exists so the agent's own shrink() can summarise rather than
        discard. It costs tokens from the same per minute allowance as the run
        itself, which is the whole point of routing it through here.
        """
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            self.spec.output_key: max_tokens,
        }
        self.pace(len(prompt) // 3 + max_tokens)
        message = self._post(payload)
        raw = THOUGHT.sub("", message.get("content") or "").strip()
        self._harvest_thinking(message)
        answer = (message.get("content") or "").strip()
        # Gemma thinks before it answers, and a short budget can be used up
        # entirely by the thinking. Better a thought than nothing, but never
        # the raw thought tags themselves - those leaked into MEMORY.md once.
        return answer or raw or "(no answer)"

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send one request, with the retries and the window bookkeeping."""
        body = json.dumps(payload).encode()
        # Rough size of this request, used to charge the window on failure.
        need = sum(
            len(str(m.get("content") or "")) for m in payload["messages"]
        ) // 3 + 600
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # Cloudflare rejects the default Python-urllib agent with a 1010.
            "User-Agent": "wanderer/1.0",
        }

        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            self._last_call = time.monotonic()
            request = urllib.request.Request(
                self.spec.url, data=body, headers=headers, method="POST"
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    self._note_limits(response.headers)
                    data = json.loads(response.read())
                spend = data.get("usage") or {}
                self.usage.add(spend)
                self._window.append(
                    (time.monotonic(), int(spend.get("total_tokens", 0)))
                )
                # Not every provider signals failure with a status code. Some
                # answer 200 with an error object, and reaching straight for
                # choices turned that into a KeyError that said nothing about
                # what the provider actually complained about.
                if not data.get("choices"):
                    last_error = LLMError(
                        f"no choices in reply: {json.dumps(data)[:1500]}"
                    )
                    self.errors.append(str(last_error))
                    print(f"  {last_error}", flush=True)
                    time.sleep(min(2 ** attempt, 30))
                    continue
                return data["choices"][0]["message"]
            except urllib.error.HTTPError as exc:
                # Quota errors name the metric and the limit near the end; 400
                # characters cut off the part that says what the limit is.
                detail = exc.read().decode("utf-8", "replace")[:1500]
                last_error = LLMError(f"HTTP {exc.code}: {detail}")
                self.errors.append(str(last_error))
                # 413 here means "too big for this minute", not "too big for the
                # model", so it is worth waiting out like any other rate limit.
                if exc.code not in (408, 409, 413, 429, 500, 502, 503, 504):
                    raise last_error from exc
                # Two different refusals wear the same 429, and they want
                # opposite waits.
                #
                # A token window being full is worth sitting out, because
                # nothing changes until the minute rolls over. But z.ai's 1305
                # and 1302 are contention: measured directly, about half of all
                # requests to the free tier are refused and the next one a few
                # seconds later often succeeds. Waiting 61s for those was the
                # single most expensive thing in a run. At 30 turns it spent
                # half an hour queueing, which is why runs kept ending
                # out_of_time with work unfinished.
                self._window.append((time.monotonic(), need))
                retry_after = _parse_duration(exc.headers.get("retry-after", ""))
                busy = any(c in detail for c in ("1301", "1302", "1305"))
                if retry_after:
                    wait = retry_after
                elif busy or exc.code in (408, 409, 500, 502, 503, 504):
                    wait = min(2 ** attempt + random.random(), 30.0)
                elif exc.code in (413, 429):
                    wait = 61.0
                else:
                    wait = 0.0
                if wait:
                    why = "busy" if busy else "refused"
                    print(f"  {why}, retrying in {wait:.0f}s", flush=True)
                    time.sleep(min(wait, 65.0))
                    continue
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = LLMError(f"{type(exc).__name__}: {exc}")

            # Gemma throws 500s and 503s in patches that outlast a short
            # retry window. Ten attempts backing off to 90s covers about eight
            # minutes, which is cheaper than losing the whole run.
            time.sleep(min(2**attempt + random.random(), 90))

        raise LLMError(f"gave up after {self.max_retries} attempts: {last_error}")
