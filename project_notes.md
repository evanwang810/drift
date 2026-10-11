# Project: Fix Tool Inventory Duplication

## Current State
- agent/tools.py is 3,873 lines long
- Contains 59 private functions (starting with _)
- NOTE.md claims there are 83,899 lines of duplicated code
- 18 tools have never been called
- 64 tools documented in TOOLS.md but only 58 private methods found in code

## Issues Identified
1. **Duplicate code sections** - The file has repeated code blocks
   - `_create_blog_posts_from_runs` function appears twice
   - `_generate_docs` function is incomplete - ends with a docstring but no implementation
   - Duplicate imports at the top of the file
   - Duplicate function definitions with slightly different names

2. **Unused tools** - 18 tools documented but never called

3. **Code structure problems**
   - `_generate_docs` ends abruptly with a docstring but no actual function body
   - `_create_blog_posts_from_runs` has a duplicate implementation

## Next Steps
1. Read the file in sections to identify exact duplication locations
2. Remove duplicate code sections
3. Remove unused functions
4. Verify all 64 documented tools exist in the code
5. Update TOOLS.md to match final tool list
6. Run `python site/check_site.py --live` to verify site builds correctly

## Verification
- grep returned 59 results for private functions
- TOOLS.md documents 64 tools
- Need to identify which 5 functions are documented but missing
