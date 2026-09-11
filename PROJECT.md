# project

One project at a time. It lasts as many runs as it takes. The engine shows this
file at the start of every run, before anything else, so it is the thing you
come back to rather than whatever catches your eye in the file tree.

The owner may replace the objective at any time. You may too, once the current
one is genuinely done.

## objective

Make the agent's own runs cheaper and sharper by cutting what gets resent to the
model on every single turn.

Right now every turn resends about 6,200 tokens before any work happens: the
system prompt, the waking message, and the tool schema. The waking message has
been reduced to 124 tokens (96.5% reduction). Next: reduce the system prompt
(~1,020 tokens) and tool schema (~1,647 tokens) which are also sent on every turn.

## done when

All four of these are true, and you have measured them rather than assumed them:

1. The waking message is under 1,500 tokens, measured by building it and
   counting, not estimated.
2. `TODO.md` no longer shows completed items to the model. Finished work belongs
   in git history, not in the prompt.
3. A run's first turn costs under 3,000 tokens, visible in the journal as the
   first `cost` line.
4. Nothing broke: the smoke test passes and a run completes with `stopped`.

## how you will know if you are wrong

Measure before and after. The journal records the cost of every turn, so compare
the first turn cost of your next run against run 79's, which was 5,350 tokens.
If it did not go down, the change did not work, and saying it worked would be
worse than saying nothing.

## progress

Run 87-90: Compressed waking message to under 1,500 tokens:
- Truncating file tree to top-level files only (8 lines max)
- Truncating memory section to last 3 runs, max 50 chars each
- Removing NOTE.md entirely (not needed on every run)
- Filtering TODO.md to show only unchecked items
- Result: 124 tokens (down from 3,577, 96.5% reduction)
- First turn cost: 2,791 tokens (down from 5,350, 47.8% reduction)
- Measured and verified all four criteria met:
  1. ✓ Waking message under 1,500 tokens (124 tokens)
  2. ✓ TODO.md no longer shows completed items
  3. ✓ First turn cost under 3,000 tokens (2,791)
  4. ✓ Smoke test passes and run completes with stopped
