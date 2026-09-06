"""An agent that wakes up in its own repository and works on what it likes.

One run is one process. It is shown the time, its memory and its files, it acts
until it stops, and then it writes a paragraph for whoever wakes up next. That
paragraph is the only thing that carries over.

engine/ and this file are fixed. Everything else is the agent's.
"""

from __future__ import annotations

import os
import re
import subprocess
import traceback
from datetime import datetime, timezone
from pathlib import Path

from agent import tools
from engine import loop, safety
from engine.llm import PROVIDERS, Client, LLMError

ROOT = Path(__file__).resolve().parent
PROVIDER = os.environ.get("PROVIDER", "gemini")
MAX_TURNS = int(os.environ.get("MAX_TURNS", "40"))
KEEP_MEMORIES = 8


def state() -> tuple[int, str, str]:
    """Run number, first-run date and last outcome, read out of MEMORY.md."""
    text = (ROOT / "MEMORY.md").read_text(encoding="utf-8") if (ROOT / "MEMORY.md").is_file() else ""
    runs = re.findall(r"^## run (\d+) \| ([\d-]+) \| (\w+)", text, re.M)
    if not runs:
        return 1, "", ""
    return int(runs[-1][0]) + 1, runs[0][1], runs[-1][2]


def remember(run: int, outcome: str, paragraph: str, now: datetime) -> None:
    """Prepend this run's paragraph and keep only the recent ones.

    Memory is a short chain, not an archive. Anything older than the last few
    runs is in git history if it is ever wanted again.
    """
    path = ROOT / "MEMORY.md"
    old = path.read_text(encoding="utf-8") if path.is_file() else ""
    entries = re.split(r"(?=^## run )", old, flags=re.M)
    entries = [e for e in entries if e.strip().startswith("## run")]
    fresh = f"## run {run} | {now:%Y-%m-%d} | {outcome}\n\n{paragraph.strip()}\n\n"
    path.write_text(
        "# memory\n\n" + fresh + "".join(entries[:KEEP_MEMORIES - 1]),
        encoding="utf-8",
    )


def log(run: int, outcome: str, note: str, turns: int, tokens: int, now: datetime) -> None:
    runs = ROOT / "RUNS.md"
    if not runs.is_file():
        runs.write_text(
            "# runs\n\nOne row per waking, written by the engine.\n\n"
            "| run | when (UTC) | outcome | turns | tokens | note |\n"
            "| --: | --- | --- | --: | --: | --- |\n",
            encoding="utf-8",
        )
    clean = " ".join(note.split())[:60].replace("|", "/") or "-"
    with runs.open("a", encoding="utf-8") as fh:
        fh.write(f"| {run} | {now:%Y-%m-%d %H:%M} | {outcome} | {turns} |"
                 f" {tokens:,} | {clean} |\n")


def journal(run: int, outcome: str, actions: list[str], now: datetime) -> None:
    """The full trace, for people. The agent is never shown this."""
    entry = [f"## run {run} - {now:%H:%M} UTC - {outcome}", ""]
    entry += [f"- {a}" for a in actions] or ["- did nothing"]
    entry += ["", "```"] + loop.TRANSCRIPT + ["```", ""]
    (ROOT / "journal").mkdir(exist_ok=True)
    with (ROOT / "journal" / f"{now:%Y-%m-%d}.md").open("a", encoding="utf-8") as fh:
        fh.write("\n".join(entry) + "\n")


def commit(note: str, run: int, outcome: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=False)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT,
                      check=False).returncode == 0:
        print("nothing changed")
        return
    subject = note.strip().splitlines()[0][:72] if note.strip() else f"run {run}"
    subprocess.run(["git", "commit", "-m", f"{subject}\n\nrun {run}, {outcome}"],
                   cwd=ROOT, check=False)


def running() -> bool:
    kill = ROOT / "KILL"
    if not kill.is_file():
        return True
    first = kill.read_text(encoding="utf-8").strip().splitlines()[:1]
    return not first or first[0].strip().upper() != "RUN=FALSE"


def main() -> int:
    spec = PROVIDERS[PROVIDER]
    key, child_env = safety.take_key(spec.key_env)
    if not running():
        print("KILL says stop")
        return 0
    if not key:
        print(f"no {spec.key_env}")
        return 1

    now = datetime.now(timezone.utc)
    run, started, last = state()
    days = (now - datetime.fromisoformat(started).replace(tzinfo=timezone.utc)).days if started else 0

    client = Client(api_key=key, provider=PROVIDER, model=os.environ.get("MODEL", ""))
    ex = tools.Executor(root=ROOT, env=child_env)
    message = os.environ.get("MESSAGE", "")

    print(f"run {run} on {client.model} | {MAX_TURNS} turns"
          f" | {client.spec.tpm:,} tokens a minute", flush=True)

    messages = loop.opening(ROOT, run, days, last, now, MAX_TURNS, message)

    try:
        outcome, note, memory = loop.run(client, ex, messages, MAX_TURNS)
    except LLMError as exc:
        outcome, note, memory = "api_error", "the api would not answer", ""
        print(exc)
    except Exception:  # noqa: BLE001 - the traceback is content
        outcome, note, memory = "crashed", "something went wrong", ""
        print(traceback.format_exc())

    ex.actions += safety.check(ROOT)

    # A run always leaves a paragraph. If it did not write one, ask for one,
    # because a run that carries nothing forward may as well not have happened.
    if not memory and loop.TRANSCRIPT:
        try:
            memory = client.ask(
                "You are an agent that just finished a work session. Below is a"
                " log of it. Write one short paragraph, first person, for"
                " yourself at the start of the next session: what you were"
                " doing, what you found, what to do next. No preamble.\n\n"
                + "\n".join(loop.TRANSCRIPT)[-6000:],
                400,
            )
            ex.actions.append("memory written for it, it did not leave one")
        except LLMError:
            memory = f"Run {run} ended as {outcome} without leaving a note."

    remember(run, outcome, memory or f"Run {run} ended as {outcome}.", now)
    journal(run, outcome, ex.actions, now)
    log(run, outcome, note, loop.TURNS, client.usage.total, now)
    safety.redact(ROOT, [key, child_env.get("GH_TOKEN", "")])
    commit(note, run, outcome)

    print(f"\n=== run {run}: {outcome} | {loop.TURNS} turns"
          f" | {client.usage.total:,} tokens")
    for action in ex.actions:
        print(f"  {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
