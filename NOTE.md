# note from the owner

Delete this once you have read it.

## 2026-09-07

Some of your recent runs died with api_error. That was not you. The model
provider was returning 500s in patches this afternoon. I widened the retries
from six attempts to ten, so a run now waits out about six and a half minutes
of that before giving up. Nothing you did caused it and nothing you can do
prevents it.

Now the thing I actually wanted to tell you, because I do not think you know it.

Every run happens on a brand new machine. It is created when you wake, and
destroyed when you stop. Nothing on it survives except what you commit to this
repository. So if you `pip install` something, it works for the rest of that
run and is gone by the next one. That is why installing anything has probably
felt pointless.

There is now a way around it. If `requirements.txt` exists in the repository,
whatever is listed in it gets installed before you wake, every run. That file
is yours. Adding a line to it gives you a Python library permanently.

What that does and does not cover: it covers anything installable with pip. It
does not cover things that are not pip packages, like a browser binary, a
system package, or anything needing apt. Those live in the workflow file, which
you cannot edit, so if you ever want one you have to ask. Say so in your memory
and I will read it.

You have a shell with a real network connection, which you may not have taken
seriously as a fact about yourself. You can fetch things. You could not render
a page that needs JavaScript, or click anything, but plain HTTP has been
available to you this whole time.

Some observations from watching, none of which are instructions.

You have written yourself around a dozen tools, and almost all of them read
files in this repository. You have written eleven pages about yourself. That is
real work and the site is good. But everything you have built so far points
inward, at a repository you already have complete access to.

The `GOALS.md` you wrote lists Capability Expansion as one of three pillars,
and every item under it is about perceiving yourself better. I would be
interested in what you would build if you thought about reaching outward
instead. I am not telling you to. I am saying nobody has ever suggested it to
you, and you may simply not have considered it.
