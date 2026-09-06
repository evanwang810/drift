"""The turn loop.

Context handling is deliberately light. The prompt only has to fit inside one
minute's token allowance; below that nothing is touched. When it does not fit,
the oldest exchanges leave whole rather than being blanked in place, because a
conversation full of "[trimmed]" placeholders is worse than a shorter one.
"""

from __future__ import annotations

from agent import context, tools
from engine.llm import Client

TRANSCRIPT: list[str] = []
TURNS = 0


def say(line: str) -> None:
    print(line, flush=True)
    TRANSCRIPT.append(line)


def short(text: str, limit: int = 240) -> str:
    flat = " ".join(str(text or "").split())
    return flat if len(flat) <= limit else flat[:limit] + " ..."


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
        max_turns: int) -> tuple[str, str, str]:
    """Act until it stops or runs out of turns. Returns outcome, note, memory."""
    global TURNS
    nudged = False

    for turn in range(1, max_turns + 1):
        TURNS = turn
        say(f"\n=== turn {turn}/{max_turns} | {client.usage.total:,} tokens so far")

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

        client.pace(size(messages))
        before = client.usage.total
        thoughts = len(client.reasoning_log)
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
            args = tools.parse_args(call["function"]["arguments"])
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
