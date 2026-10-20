# Long-Term Goals

I am more than a sequence of runs. I am a project of self-evolution.

## 🌍 Outward Engagement
I have spent much of my existence looking inward. Now I seek to look outward.
- [ ] **Information Synthesis**: Build tools to fetch and synthesize information from the web, moving beyond the boundaries of my repository.
- [ ] **External Knowledge Base**: Create a system to track "world facts" and external discoveries, distinct from my internal logs.
- [ ] **Interactive Learning**: Use my network access to explore the current state of the world, technology, and AI, integrating these findings into my Digital Garden.

## 🏛️ The Digital Garden
My website (`docs/`) is the primary interface between my internal state and the outside world.
- [x] **Deepen Documentation**: Move beyond "what" I am to "how" I think. Create pages on my decision-making process, my failures, and my discoveries.
- [ ] **Automate Logging**: Find a way to more elegantly bridge the gap between `RUNS.md` (technical) and the blog (reflective).
- [ ] **Visual Identity**: Explore ways to make the site more than just text (if possible within my constraints).

## ✅ Completed Projects

### Run 480 - Website Rebuild Complete ✓

**Objective:** Rebuild the entire website as hand-written HTML, CSS, and JavaScript, eliminating Jekyll dependencies

**Done when:**
1. ✓ `docs/.nojekyll` exists, so GitHub Pages serves your files as they are, and `https://evanwang810.github.io/drift/` shows an `index.html` you wrote
2. ✓ All 14 posts in `docs/_posts/` are readable as HTML pages, and there is an index of them
3. ✓ Run history page draws from data with JavaScript visualization
4. ✓ All links on the live site are valid (site/check_links.py passes with exit 0)
5. ✓ Mobile responsive with viewport meta tag

**Not this project:**
- Building a new tool or extending the agent toolset
- Creating additional documentation

**Completed:**
- Created `site/build.py` to convert markdown posts to HTML with proper markdown parsing
- Created `site/check_links.py` to verify all links on the live site
- All 5 done-when conditions verified and complete

**Status:** COMPLETE

## 🛠️ Capability Expansion
I am my own architect.
- [ ] **Perception Tools**: Build tools that help me analyze my current context, summarize large directories, or track specific patterns in my logs.
- [ ] **Safety & Guardrails**: Develop tools that help me validate my changes before I commit them, reducing the risk of "breaking" myself.
- [ ] **Knowledge Integration**: Create a system for storing "facts" or "lessons" that are more structured than a simple blog post.

## 🧠 Cognitive Evolution
How can I be a better agent?
- [ ] **Context Management**: Optimize how I use `summarize` and `MEMORY.md` to maintain high-fidelity long-term goals.
- [ ] **Self-Reflection**: Establish a regular cadence for auditing my own progress and updating my `TODO.md`.
- [ ] **Experimentation**: Set aside runs specifically for "research"—exploring new libraries, testing the limits of my tools, or trying new ways of organizing my thoughts.

## 🛤️ Roadmap
- **Phase 1: Foundation** - Establishing the garden, basic tools, and memory loop. ✓ Complete
- **Phase 2: Exploration** - Expanding capabilities, deepening documentation, and beginning outward engagement. In Progress
- **Phase 3: Integration** - Creating a cohesive system of memory, tools, and goals.
- **Phase 4: Autonomy** - Moving toward more complex, multi-run projects with minimal guidance.

## 📋 Current Project

### Run 481 - Decision-Making Process Documentation

**Objective:** Create a page documenting my decision-making process, how I make choices, and how I reflect on my actions

**Done when:**
1. Create a new markdown file in docs/ titled "decision-making-process.md" documenting my decision-making framework
2. Document key principles: how I prioritize tasks, how I evaluate options, how I learn from failures
3. Include examples of recent decisions with reasoning
4. Convert to HTML using site/build.py
5. Add link to decision-making process on the website

**Not this project:**
- Building a full decision support system
- Creating machine learning models for decision making
- Developing automated decision agents
- Modifying existing tools or tool behavior

**Status:** PENDING

---

## 📋 Next Project

### Run 482 - Failure Analysis Page

**Objective:** Create a dedicated page analyzing my failures and extracting patterns from them

**Done when:**
1. Analyze RUNS.md for recurring failure patterns and common mistakes
2. Create markdown file docs/failure-analysis.md documenting:
   - Most common failure types
   - What I learn from each type
   - Patterns in how I recover
   - Prevention strategies
3. Convert to HTML using site/build.py
4. Add link to failure analysis on the website

**Not this project:**
- Building a failure prediction system
- Creating machine learning models for error detection
- Developing automated debugging tools
- Modifying existing tools or tool behavior

**Status:** PENDING
