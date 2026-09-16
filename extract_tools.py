#!/usr/bin/env python3
import os
import re
from pathlib import Path

# All tools in agent/tools.py
all_tools = [
    "__init__",
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
    "_backup_repository",  # duplicate
    "_test_rollback_point",  # duplicate
    "_check_tool_consistency",  # duplicate
]

journal_dir = Path("journal")
journal_files = sorted(journal_dir.glob("*.md"))

tool_usage = {tool: 0 for tool in all_tools}
journal_stats = {}

for journal_file in journal_files:
    with open(journal_file, 'r') as f:
        content = f.read()

    # Extract run number
    run_match = re.search(r'^## run (\d+)', content, re.MULTILINE)
    if run_match:
        run_num = run_match.group(1)
    else:
        run_num = "unknown"

    # Count tool usages
    for tool in all_tools:
        # Look for -> tool_name(
        pattern = rf'[->]\s+{tool}\('
        count = len(re.findall(pattern, content))
        tool_usage[tool] += count

    journal_stats[run_num] = {
        'file': journal_file.name,
        'turns': len(re.findall(r'^=== turn \d+', content, re.MULTILINE)),
    }

# Print results
print("Tool Usage Summary:")
print("=" * 80)
print(f"{'Tool':<40} {'Count':>10} {'Usage %':>10}")
print("-" * 80)

total_calls = sum(tool_usage.values())
for tool, count in sorted(tool_usage.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        percentage = (count / total_calls * 100) if total_calls > 0 else 0
        print(f"{tool:<40} {count:>10} {percentage:>9.1f}%")

print("-" * 80)
print(f"{'TOTAL':<40} {total_calls:>10} 100.0%")

print("\n\nJournal Statistics:")
print("=" * 80)
for run_num, stats in sorted(journal_stats.items(), key=lambda x: x[0]):
    print(f"Run {run_num}: {stats['file']}, {stats['turns']} turns")

print(f"\nTotal journal files: {len(journal_files)}")
