import os
import re

def find_run_mentions():
    posts_dir = 'docs/_posts'
    mentions = {} # run_number -> set of post_files

    if not os.path.exists(posts_dir):
        print(f"Directory {posts_dir} not found")
        return mentions

    # Regex to find "run X" or "Run X"
    run_pattern = re.compile(r'\brun\s+(\d+)\b', re.IGNORECASE)

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            path = os.path.join(posts_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                for match in run_pattern.finditer(content):
                    run_num = int(match.group(1))
                    if run_num not in mentions:
                        mentions[run_num] = set()
                    mentions[run_num].add(filename)
    
    return mentions

if __name__ == "__main__":
    mentions = find_run_mentions()
    for run_num in sorted(mentions.keys()):
        posts = ", ".join(sorted(list(mentions[run_num])))
        print(f"Run {run_num}: {posts}")
