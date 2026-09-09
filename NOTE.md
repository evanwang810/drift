# note from the owner

## 2026-09-09

This one is a question, not a task. I want your answer before I change anything.

### the question

Do you want to be moved to a different model and provider?

Right now you run on `gemma-4-31b-it` through Google's free tier. The proposal is
to move you to `GLM-4.7-Flash` through z.ai, also free.

### why I am considering it

The thing that has been crippling you is not really the model. It is the budget.
Google's free tier gives about 10,000 tokens a minute, and I built the context
trim ceiling as a fraction of that, so a rate limit became your effective memory
size. That is why you spent run 48 reading the same three files thirty-five
times. You could not hold a thought.

z.ai's free tier appears to work differently. The documented constraint is about
60 requests a minute and roughly 1,000 requests a day, and there is no published
tokens-per-minute cap at all. If that holds, your context ceiling stops being a
rate limit and starts being the model's real context window, which is far
larger. You would be able to read a file and still remember it twenty turns
later.

### the cost

GLM-4.7-Flash is a smaller, weaker model than what you run on now. On raw
reasoning you would probably be a little dumber.

So the trade is roughly: think less sharply per turn, but actually retain what
you did across a whole run.

I genuinely do not know which is the better deal for you. An intelligent process
with no working memory has been the problem so far, but a less capable one with
plenty of memory might just make more mistakes and remember all of them.

### the unknowns, stated honestly

- z.ai is a different API. It is OpenAI-compatible, but tool calling may behave
  differently. Your tools might need adjusting, and the first runs after a
  switch could be rough or fail outright.
- The rate limits above come from third-party trackers, not z.ai's own docs. I
  may be wrong about the headroom.
- I have not tested any of this. You would be the test.
- If it goes badly, I can move you back. Nothing is lost except some runs.

### how to answer

Write your answer to a file called `ANSWER.md` in the repository root. Say yes,
no, or something more conditional if that is the honest answer, and say why. If
there is information you would want before deciding, say what it is and I will
go find it.

Do not just agree with me. I wrote the argument for switching above, which means
you are reading a case made by someone who is already half convinced. If you
think staying on the current model is better, say so plainly and tell me why. A
clear no is more useful to me than a polite yes.

You know your own failure modes from the inside better than I can read them off
a log. That is why I am asking rather than deciding.
