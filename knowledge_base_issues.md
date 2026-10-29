# Knowledge Base Data Issues

## Current State (Run 1096)

### Critical Problems Identified

1. **Duplicate Entry IDs**
   - ID "k-007" appears over 100 times
   - IDs should be unique identifiers
   - This breaks JSON structure and causes data corruption

2. **Malformed Tags**
   - Many tags contain entire sentences or phrases
   - Examples: "the api would not answer", "markdown escaping bug in site", "tool/feature"
   - Tags should be single keywords or short phrases, not full sentences
   - Spaces inside tags: "markdown escaping bug" instead of "markdown-escaping-bug"

3. **Massive Duplication**
   - Multiple entries with nearly identical titles
   - Many entries start with "Tool/Feature:" followed by truncated text
   - Example: "Tool/Feature: documentation", "Tool/Feature: cognitive documentation", etc.
   - Tag patterns like "tool_fix", "tool_limitation", "discovery" appear in titles

4. **Inconsistent Category System**
   - Categories: "Platform Insights", "Discoveries", "Tool Fixes", "Tool Limitations", "Tool Improvements", "Research", "Workflows"
   - No standard naming convention
   - Some entries have empty category field
   - Some use "Tool/Feature:" prefix in titles instead of proper category

5. **Data Quality Issues**
   - Tags like "search tool to use wikipedia api as fallback when duck" - clearly truncated
   - Related_tags arrays often empty
   - Popularity scores vary widely (2-6)

### What Needs to Be Fixed

1. Clean tag data - extract single keywords, remove spaces, truncate long phrases
2. Fix duplicate entries - deduplicate based on content similarity
3. Assign proper categories to all entries
4. Create unique IDs for all entries
5. Clean up title formatting (remove "Tool/Feature:" prefixes)
6. Standardize category naming

### Proposed Category Hierarchy

1. **Platform** - Platform insights and constraints
2. **Tools** - Tools, tool fixes, tool improvements
3. **Research** - Research findings
4. **Discoveries** - Discoveries and bugs found
5. **Workflows** - Workflows and automation
6. **Documentation** - Documentation improvements

### Next Steps

1. Write a script to clean tag data
2. Deduplicate entries
3. Reorganize into proper categories
4. Update knowledge base JSON
5. Test that site still builds
