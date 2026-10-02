"""Whether the website project is done. Written by the owner; please do not edit it.

Run it after every change to the site:

    python site/check_site.py           checks the files in docs/
    python site/check_site.py --live    checks the published site

Each line is PASS or FAIL with the reason. The project is done when every line
passes on --live. Until then it is not done, whatever memory says.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
LIVE = "https://evanwang810.github.io/drift/"
POSTS = sorted(p.stem for p in (DOCS / "_posts").glob("*.md"))


def fetch(name: str, live: bool) -> str | None:
    if live:
        try:
            with urllib.request.urlopen(LIVE + name, timeout=20) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001 - a page that will not load is a failure
            return None
    path = DOCS / name
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else None


def links(html: str) -> list[str]:
    found = re.findall(r'href="([^"#?]+)', html)
    return [h for h in found if not h.startswith(("http:", "https:", "mailto:"))]


def main() -> int:
    live = "--live" in sys.argv
    results: list[tuple[bool, str]] = []

    def check(ok: bool, what: str) -> None:
        results.append((ok, what))

    index = fetch("index.html", live)
    check(index is not None, "index.html exists")
    index = index or ""

    # Every post reachable from the home page, directly or through one page it links to.
    reachable = set(links(index))
    for page in list(reachable):
        if page.endswith(".html") and page != "index.html":
            reachable |= set(links(fetch(page, live) or ""))
    missing = [p for p in POSTS if f"{p}.html" not in reachable]
    check(not missing, f"all {len(POSTS)} posts are linked from the home page or a page it links to"
          + (f"; not reachable: {', '.join(missing[:4])}{' ...' if len(missing) > 4 else ''}" if missing else ""))

    # Posts render as HTML, not as markdown.
    bad = []
    for post in POSTS:
        html = fetch(f"{post}.html", live)
        if html is None:
            bad.append(f"{post} (missing)")
        elif "```" in html or re.search(r"<p>\s*<h\d", html) or re.search(r"<h(\d)>[^<]*\n", html):
            bad.append(post)
    check(not bad, "every post renders: no literal ``` and no broken headings"
          + (f"; wrong: {', '.join(bad[:4])}" if bad else ""))

    # runs.json holds every run, with real numbers.
    rows = re.findall(r"^\| (\d+) \|", (ROOT / "RUNS.md").read_text(encoding="utf-8"), re.M)
    raw = fetch("runs.json", live)
    try:
        data = json.loads(raw or "")
    except json.JSONDecodeError:
        data = None
    if not isinstance(data, list):
        check(False, "runs.json is a JSON list")
    else:
        # The live copy lags by however many runs happened since the last push.
        check(len(data) >= len(rows) - (5 if live else 1),
              f"runs.json has every run: {len(data)} entries, RUNS.md has {len(rows)}")
        tokens = [r.get("tokens") for r in data if isinstance(r, dict)]
        nonzero = sum(1 for t in tokens if isinstance(t, (int, float)) and t > 0)
        check(nonzero >= len(tokens) * 0.8,
              f"runs.json has token counts: {nonzero} of {len(tokens)} entries are above zero")

    # The timeline page reads that data and draws it.
    runs_page = fetch("runs.html", live) or ""
    check("runs.json" in runs_page and "<script" in runs_page,
          "runs.html loads runs.json with a script")
    check(bool(re.search(r"<svg|<canvas|createElementNS|getContext", runs_page)),
          "runs.html draws with SVG or canvas")

    # No dead links from any page the home page links to.
    pages = ["index.html"] + sorted({p for p in links(index) if p.endswith(".html")})
    dead = []
    for page in pages:
        for target in links(fetch(page, live) or ""):
            if fetch(target, live) is None:
                dead.append(f"{page} -> {target}")
    check(not dead, "no dead links on the home page or the pages it links to"
          + (f"; dead: {', '.join(sorted(set(dead))[:4])}" if dead else ""))

    check("viewport" in index and "viewport" in runs_page, "pages have a viewport meta tag")

    for ok, what in results:
        print(("PASS  " if ok else "FAIL  ") + what)
    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - failed} of {len(results)} pass"
          + ("" if live else ". Run with --live after pushing to check the published site."))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
