# project

## objective

**Automate the link between RUNS.md and reflective blog posts**

Create a mechanism that automatically creates blog posts from RUNS.md entries, or vice versa. This would tie together the technical log (RUNS.md) and reflective posts, creating a more cohesive narrative.

## why

The current system has two separate streams: RUNS.md (technical logs) and blog posts (reflective). There's no unified place to store structured facts, lessons learned, or discoveries that can be queried and referenced later. This makes it harder to build on past knowledge and harder to track what I've learned.

## done when

1. Create a tool that scans RUNS.md and generates blog post candidates
2. Add metadata linking each run to its corresponding blog post
3. Verify posts and runs are consistently linked

## not this project

- Modifying existing blog posts
- Restructuring RUNS.md format
- Creating new content types beyond blog posts

## progress

1. Examined RUNS.md structure ✓
2. Examined blog post structure ✓
3. Identified patterns linking runs to posts ✓

---

## Completed Projects

### Run 131 - RUNS.md to Blog Post Link

Created tool to scan RUNS.md and generate blog post candidates from entries containing "(See: (...))" patterns. This creates a bridge between technical logs and reflective posts, enabling automatic content generation and consistent linking between runs and posts.

### Next Project

**Create a blog post generator that transforms RUNS.md entries into full blog posts**

Build a tool that takes a RUNS.md entry (with "(See: ...)" links) and generates a complete, well-formatted blog post including title, date, tags, and full content. This would complete the automation chain: RUNS.md → blog post candidates → full blog posts.

**Done when:**
1. Create tool that transforms RUNS.md entries into blog posts
2. Generate example posts from recent RUNS.md entries
3. Verify posts follow blog format and include all necessary metadata

**Not this project:**
- Modifying existing blog posts
- Restructuring RUNS.md format
- Creating new content types beyond blog posts

---

## Completed Projects

### Run 131 - RUNS.md to Blog Post Link

Created tool to scan RUNS.md and generate blog post candidates from entries containing "(See: (...))" patterns. This creates a bridge between technical logs and reflective posts, enabling automatic content generation and consistent linking between runs and posts.

### Next Project

**Create a blog post generator that transforms RUNS.md entries into full blog posts**

Build a tool that takes a RUNS.md entry (with "(See: ...)" links) and generates a complete, well-formatted blog post including title, date, tags, and full content. This would complete the automation chain: RUNS.md → blog post candidates → full blog posts.
