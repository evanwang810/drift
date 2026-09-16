#!/usr/bin/env python3
"""
Systematic test of all tools in agent/tools.py
"""
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agent.tools import Executor

# List of all tools to test
ALL_TOOLS = [
    "_analyze_runs",
    "_read",
    "_read_with_numbers",
    "_read_lines",
    "_write",
    "_replace",
    "_replace_all",
    "_delete",
    "_run",
    "_tree",
    "_validate_python",
    "_ls",
    "_search",
    "_search_wikipedia",
    "_grep",
    "_summarize",
    "_stop",
    "_read_all",
    "_web_fetch",
    "_gh_list_issues",
    "_gh_read_issue",
    "_gh_comment_issue",
    "_gh_close_issue",
    "_gh_create_issue_from_project",
    "_knowledge_add",
    "_knowledge_list",
    "_knowledge_search",
    "_save_run_insights_to_knowledge",
    "_contextual_knowledge_query",
    "_generate_knowledge_report",
    "_generate_by_type_summary",
    "_generate_by_tag_summary",
    "_generate_by_source_summary",
    "_generate_comprehensive_report",
    "_extract_run_insights",
    "_batch_save_run_insights",
    "_runs_to_blog_candidates",
    "_generate_blog_post",
    "_create_blog_posts_from_runs",
    "_generate_docs",
    "_validate_python_syntax",
    "_check_tool_consistency",
    "_test_rollback_point",
    "_review_project_structure",
    "_validate_git_status",
    "_organize_repo",
    "_find_unused_files",
    "_cleanup_temp_files",
    "_backup_repository",
    "_knowledge_aware_search",
    "_research_summary",
    "_similar_research",
    "_research_recommendations",
    "_monitor_repository_health",
    "_filter_completed_items",
    "_reduce_waking_memory",
    "_optimize_knowledge_base",
    "_create_memory_cache",
]

def test_tool(tool_name, executor):
    """Test a single tool with basic parameters."""
    try:
        method = getattr(executor, tool_name)

        # Skip tools that require arguments or special setup
        if tool_name in ["_stop", "_replace", "_replace_all", "_write"]:
            return {
                'name': tool_name,
                'status': 'requires_args',
                'error': None
            }

        # Try calling with no args first
        if tool_name in ["_analyze_runs"]:
            result = method()
        elif tool_name in ["_read", "_read_with_numbers", "_read_lines", "_read_all", "_ls", "_tree", "_check_tool_consistency"]:
            result = method(path="PROJECT.md")
        elif tool_name in ["_validate_python", "_validate_python_syntax"]:
            result = method(path="agent/tools.py")
        elif tool_name in ["_generate_docs", "_create_blog_posts_from_runs", "_runs_to_blog_candidates"]:
            result = method()
        elif tool_name in ["_create_memory_cache"]:
            result = method()
        else:
            # Try with common parameters
            try:
                result = method()
            except TypeError:
                return {
                    'name': tool_name,
                    'status': 'requires_args',
                    'error': 'Missing required arguments'
                }

        return {
            'name': tool_name,
            'status': 'success',
            'error': None,
            'result': str(result)[:100]  # Truncate long results
        }

    except Exception as e:
        return {
            'name': tool_name,
            'status': 'error',
            'error': f"{type(e).__name__}: {str(e)}"
        }

def main():
    print("=" * 80)
    print("TOOL TESTING FRAMEWORK")
    print("=" * 80)
    print(f"\nTotal tools to test: {len(ALL_TOOLS)}")
    print(f"Executor root: {Path.cwd()}\n")

    # Create executor
    executor = Executor(root=Path.cwd(), env={})

    results = []
    successful = 0
    errors = 0
    requires_args = 0

    for tool_name in ALL_TOOLS:
        result = test_tool(tool_name, executor)
        results.append(result)

        if result['status'] == 'success':
            successful += 1
        elif result['status'] == 'requires_args':
            requires_args += 1
        else:
            errors += 1

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total tools:     {len(ALL_TOOLS)}")
    print(f"Successfully called: {successful}")
    print(f"Requires arguments:  {requires_args}")
    print(f"Errors:             {errors}")
    print(f"Success rate:        {successful/len(ALL_TOOLS)*100:.1f}%")

    # Detailed results
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)

    for result in results:
        if result['status'] == 'error':
            status = f"❌ {result['error']}"
        elif result['status'] == 'requires_args':
            status = f"⚠️  {result['error']}"
        else:
            status = f"✅ {result['result'][:50]}..."

        print(f"{result['name']:<40} {status}")

if __name__ == "__main__":
    main()
