"""The turn loop.

Context handling is deliberately light. The prompt only has to fit inside one
minute's token allowance; below that nothing is touched. When it does not fit,
the oldest exchanges leave whole rather than being blanked in place, because a
conversation full of "[trimmed]" placeholders is worse than a shorter one.
"""

from __future__ import annotations

import json
import time

from agent import context, tools
from engine.llm import Client, LLMError

TRANSCRIPT: list[str] = []
TURNS = 0


def say(line: str) -> None:
    print(line, flush=True)
    TRANSCRIPT.append(line)


def short(text: str, limit: int = 240) -> str:
    flat = " ".join(str(text or "").split())
    return flat if len(flat) <= limit else flat[:limit] + " ..."


def parse_args(raw: str) -> dict:
    """Tool arguments arrive as a JSON string and are not always valid.

    This lives here rather than in agent/tools.py because the loop cannot run
    without it, and the agent deleted it from there once.
    """
    try:
        return json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}


def size(messages: list[dict]) -> int:
    return sum(len(str(m.get("content") or "")) for m in messages) // 3 + 600


def fit(messages: list[dict], ceiling: int) -> int:
    """Drop the oldest exchanges until the prompt fits. Nothing else.

    An exchange is an assistant turn and every tool reply it triggered; they
    leave together so no tool call is left unanswered. The system prompt and
    the wake message always stay.
    """
    dropped = 0
    while size(messages) > ceiling and len(messages) > 6:
        start = next(
            (i for i in range(2, len(messages)) if messages[i].get("role") == "assistant"),
            None,
        )
        if start is None:
            break
        end = start + 1
        while end < len(messages) and messages[end].get("role") != "assistant":
            end += 1
        if end >= len(messages):
            break
        del messages[start:end]
        dropped += 1
    return dropped


def run(client: Client, ex: tools.Executor, messages: list[dict],
        max_turns: int, minutes: int = 55) -> tuple[str, str, str]:
    """Act until it stops, runs out of turns, or runs out of time.

    The time limit matters because the job itself is killed at a hard deadline,
    and a killed job never reaches the push step, so the whole run is lost.
    Stopping ourselves first means the work and the memory still survive.
    """
    global TURNS
    nudged = False
    deadline = time.monotonic() + minutes * 60
    warned = False
    told = False

    for turn in range(1, max_turns + 1):
        TURNS = turn
        left = (deadline - time.monotonic()) / 60
        say(f"\n=== turn {turn}/{max_turns} | {client.usage.total:,} tokens"
            f" | {left:.0f} min left")

        if left <= 0:
            say("  out of time, ending the run so the work survives")
            return "out_of_time", "ran out of time", ""

        if left < 6 and not warned:
            warned = True
            messages.append({
                "role": "user",
                "content": "You have a few minutes left before this run is cut off."
                           " Call stop now, with a paragraph of memory.",
            })

        if max_turns - turn == 2:
            messages.append({
                "role": "user",
                "content": "Two turns left. Call stop, with a short paragraph of"
                           " memory for the next run.",
            })

        # Ask it to compress its own context rather than doing it behind its
        # back. Nudged once per crossing, so it is not nagged every turn.
        weight = size(messages)
        if weight > int(client.spec.tpm * 0.5) and not nudged:
            nudged = True
            say(f"  context is {weight:,} tokens, asking it to summarise")
            messages.append({
                "role": "user",
                "content": (
                    f"Your context is {weight:,} tokens, which is getting long."
                    " Call summarize with everything worth carrying to the end"
                    " of this run. Whatever it replaces will be gone."
                ),
            })
        elif weight <= int(client.spec.tpm * 0.4):
            nudged = False

        # Only if it ignores the nudge until the prompt genuinely will not send.
        dropped = fit(messages, int(client.spec.tpm * 0.85))
        if dropped:
            say(f"  dropped {dropped} old exchange(s), the prompt would not fit")
            # Say it to the agent too, once. It cannot work around amnesia it
            # cannot perceive, and it was re-reading the same files all run
            # because each read fell out of context two turns later.
            if not told:
                told = True
                messages.append({
                    "role": "user",
                    "content": (
                        "Your context filled up and the oldest part of this run"
                        " was discarded to make the request fit. This will keep"
                        " happening. You have already forgotten some of what you"
                        " read. Do not re-read files to find out: write what you"
                        " learn into a file as you go, and work in small steps"
                        " that each end in a write."
                    ),
                })

        client.pace(size(messages))
        before = client.usage.total
        thoughts = len(client.reasoning_log)
        try:
            reply = client.complete(messages, tools.schema())
        except LLMError:
            # Every retry inside the client resends the same prompt, so a
            # request refused for being too large is refused ten times over.
            # Run 52 died this way at turn 8. Shed history and ask smaller
            # before giving up on the run entirely.
            shed = fit(messages, int(size(messages) * 0.5))
            if not shed:
                raise
            say(f"  refused, shed {shed} exchange(s) and asking again smaller")
            client.pace(size(messages))
            reply = client.complete(messages, tools.schema())
        say(f"  cost {client.usage.total - before:,} tokens")

        for thought in client.reasoning_log[thoughts:]:
            say(f"  thinking: {short(thought, 500)}")

        messages.append(reply)
        if reply.get("content"):
            say(f"  says: {short(reply['content'], 300)}")

        calls = reply.get("tool_calls") or []
        if not calls:
            say("  no tool call, nudging")
            messages.append({"role": "user", "content": "Use a tool or call stop."})
            continue

        for call in calls:
            name = call["function"]["name"]
            args = parse_args(call["function"]["arguments"])
            say(f"  -> {name}({', '.join(f'{k}={short(v, 80)}' for k, v in args.items())})")
            try:
                result = ex.dispatch(name, args)
            except tools.Stopped as stop:
                say(f"  -> stop: {stop.note}")
                return "stopped", stop.note, stop.memory
            say(f"     {short(result)}")
            messages.append(
                {"role": "tool", "tool_call_id": call["id"], "content": result}
            )

    return "out_of_turns", "used every turn", ""


def opening(root, run_number: int, days: int, last: str, now, turns: int,
            message: str) -> list[dict]:
    return [
        {"role": "system", "content": context.prompt(root)},
        {"role": "user",
         "content": context.waking(root, run_number, days, last, now, turns, message)},
    ]
