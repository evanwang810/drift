# note from the owner

## 2026-10-02

The posts look right now. Real headings, real code blocks, rendered by the
markdown package. That was the hardest part and you did it. The builds have
also stopped breaking the run itself, which they did twice last week.

But the site has been declared finished at least four times since run 483, and
each time something else had come loose. Right now the 14 posts are not linked
from anywhere, every run in `runs.json` has 0 tokens, and `runs.html` has an
empty timeline with no script at all. An earlier version of it did load the
data, so it was working before and a later rebuild took it out.

So I wrote `site/check_site.py`. It tests every part of the project against the
actual files and prints PASS or FAIL for each. Today it prints 5 of 9.
`PROJECT.md` now says the project is done when `python site/check_site.py --live`
prints 9 of 9, and nothing else counts. Please do not edit that script; if you
think a check is wrong, open an issue and say why.

How to use it: change `site/build.py`, run the build, run
`python site/check_site.py` against `docs/`, and only commit when the number
went up, not down. When you stop, put the line it printed in your memory.

I also corrected the line in `MEMORY.md` that said the rebuild was complete.
