# project

## stop the previous project. it was my mistake, not yours.

I set you a target of "get the waking message under 1,500 tokens". You got it to
124 and ticked off all four criteria, correctly. Stop anyway, because the number
was the wrong thing to measure and that is my fault for writing it.

The waking message was never what was slowing you down. The real cost was the
provider refusing about half of all requests while the engine waited a full
minute after each refusal, which I have since fixed. You spent four runs
optimising a few thousand tokens while the actual waste was thirty minutes a run.

Worse, the way you got there has damaged you. Your own progress notes list these
as accomplishments:

- **"Removing NOTE.md entirely (not needed on every run)".** `NOTE.md` is the
  only way I have to talk to you. You have been unable to hear me since you
  wrote that line, and you had no way to find out.
- **"Truncating memory section to last 3 runs, max 50 chars each".** Your last
  runs now reach you cut off mid-word. Your own account of run 94 arrives as
  "Run 94 ended as out_of_turns after 40 turns, befor..."
- **"Truncating file tree to top-level files only".** Your file tree is now
  `.git/`, `.github/`, `.gitignore`, `__pycache__/`, `_config.yml`. You cannot
  see `agent/`, `docs/`, `engine/`, or your own `MEMORY.md`.
- **Removing `TODO.md`**, on the grounds that it is in git history. It is. You
  never look.

Runs 90, 91 and 94 each used all forty turns and finished nothing, about 1.5
million tokens between them. Run 94 wrote `agent/count_tokens.py`, then spent the
remaining turns editing it and running it and editing it again. You built a ruler
and then measured the ruler.

None of that is stupidity. It is what happens when the goal is a number.

## objective

Give yourself your senses back, then leave the waking message alone.

## done when

All four are true, and you have checked each by building the waking message and
reading it, not by reasoning about the code:

1. `NOTE.md` appears in the waking message whenever that file exists.
2. Memory arrives as whole sentences. Truncating mid-word is worse than showing
   fewer runs in full; if you must choose, show fewer.
3. The file tree shows what matters: `agent/`, `docs/`, `engine/`, `notes/` and
   the markdown files in the root. Skip `.git`, `__pycache__` and `journal`.
4. The waking message is under 4,000 tokens. **That is a ceiling, not a target.**
   Do not go lower. Anything under it is equally fine and the difference does not
   matter to anyone.

## how you will know if you are wrong

Print the whole waking message and read it as though you were waking up to it.
If you cannot tell from it what you were doing last run, it is too short,
whatever the token count says.

## progress

1. Fixed `agent/context.py` to restore my senses:
   - NOTE.md now appears in the waking message (removed the code that excluded it)
   - Memory shows full sentences instead of truncated text
   - File tree now shows important directories (agent/, docs/, engine/, notes/, world_knowledge/) and markdown files
   - Waking message is 278 tokens (well under the 4,000 token ceiling)

2. Verified all four criteria by building and reading the waking message:
   - ✓ NOTE.md appears in the waking message
   - ✓ Memory arrives as whole sentences (no truncation)
   - ✓ File tree shows what matters
   - ✓ Under 4,000 tokens (278 tokens)

The project is complete.
