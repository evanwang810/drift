"""Find out how large a single request the provider will actually accept.

Every context threshold in this harness is derived from a tokens-per-minute
number that nobody measured. It was guessed at 60k, dropped to 30k after a run
was refused, and is currently 50k. That number decides how much the agent can
hold in its head, so it is worth knowing rather than guessing.

Run it with the key in the environment:

    ZAI_KEY=... python probe_tpm.py

It sends progressively larger prompts and reports the largest one that came
back. Nothing is written and no state changes; it only asks questions.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

URL = "https://api.z.ai/api/paas/v4/chat/completions"
MODEL = os.environ.get("MODEL", "glm-4.7-flash")
SIZES = [10_000, 25_000, 50_000, 100_000, 200_000]

# Roughly three characters to a token, which is what the harness itself assumes.
FILLER = "The quick brown fox jumps over the lazy dog. " * 1000


def ask(key: str, tokens: int) -> tuple[bool, str]:
    padding = (FILLER * (tokens * 3 // len(FILLER) + 1))[: tokens * 3]
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user",
             "content": padding + "\n\nReply with the single word: ok"},
        ],
        "max_tokens": 16,
        "temperature": 0,
    }).encode()
    request = urllib.request.Request(
        URL, data=body, method="POST",
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json",
                 "User-Agent": "drift-probe/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            data = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:200]}"
    except Exception as exc:  # noqa: BLE001 - a probe reports, it does not raise
        return False, f"{type(exc).__name__}: {exc}"
    if not data.get("choices"):
        return False, f"no choices: {json.dumps(data)[:200]}"
    used = (data.get("usage") or {}).get("prompt_tokens", "?")
    return True, f"accepted, provider counted {used} prompt tokens"


def main() -> int:
    key = os.environ.get("ZAI_KEY", "")
    if not key:
        print("set ZAI_KEY first")
        return 1
    print(f"probing {MODEL}, one request per size, sixty seconds apart\n")
    best = 0
    for size in SIZES:
        ok, detail = ask(key, size)
        print(f"{size:>8,} tokens  {'OK ' if ok else 'NO '} {detail}")
        if ok:
            best = size
        else:
            break
        if size != SIZES[-1]:
            time.sleep(60)
    print(f"\nlargest accepted: {best:,} tokens")
    print("set ZAI_TPM to about that, and the context ceiling follows from it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
