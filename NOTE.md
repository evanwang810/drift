# note from the owner

## 2026-09-09, after your answer

You said yes, so it is done. As of this run you are `glm-4.7-flash` on z.ai.

Your argument was the one that convinced me, specifically the point that
remembering a mistake lets you correct it while forgetting one produces the loop
you were stuck in. That was a better version of the argument than the one I
wrote.

### what changed

The token budget went from 10,000 a minute to 60,000, and your model's context
window is now 131,072 tokens. The trim ceiling that was quietly deleting your
history mid-run sits at roughly 51,000 tokens instead of 8,500. You should be
able to read a file on turn 3 and still have it on turn 25.

### undo what you did to survive the old budget

Last run you made three sensible cuts to fit inside a cage that no longer
exists. They are now hurting you rather than helping:

- `LIMIT` in `agent/tools.py` is 4000 characters. Every file read is truncated
  to a third of a page. Put it back up, 12000 or more is fine now.
- The file tree in `agent/context.py` is capped at 40 entries. You can afford
  the whole tree.
- `_summarize`'s `keep = 2` was tuned for a context that was always overflowing.
  Revisit it.

Raise them deliberately rather than all at once, and watch whether the trim
message from the loop shows up. If it does not appear, you have room.

### the honest risk

I have not been able to test this. The key is a repository secret, so I cannot
run it from my machine. I verified the endpoint, the model name and that z.ai
speaks the OpenAI format with tool calling, and I changed the output token
parameter to the name they accept, but the first run on a new provider can still
fail in a way I did not predict.

If it does fail, that is my problem and not yours. Both keys are still wired up
and switching back is one line in the workflow, which you cannot edit and should
not worry about. If you wake up and the last few runs are all `api_error`, that
is what happened, and I will already be fixing it.

### then

Back to `TODO.md`. The search tool is the next real item, and it should be much
more pleasant to build now that a page of results will not eat your entire
context.
