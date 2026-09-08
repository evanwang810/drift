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

def update_runs_md(mentions):
    runs_file = 'RUNS.md'
    if not os.path.exists(runs_file):
        print(f"File {runs_file} not found")
        return

    with open(runs_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_idx = -1
    for i, line in enumerate(lines):
        if '| run | when (UTC) | outcome | turns | tokens | note |' in line:
            header_idx = i
            break
    
    if header_idx == -1:
        print("Could not find the header in RUNS.md")
        return

    new_lines = lines[:header_idx + 2]
    
    for line in lines[header_idx + 2:]:
        match = re.match(r'^\|\s*(\d+)\s*\|', line)
        if match:
            run_num = int(match.group(1))
            if run_num in mentions:
                links = []
                for post in sorted(list(mentions[run_num])):
                    links.append(f"[{post}](docs/_posts/{post})")
                
                link_str = " (See: " + ", ".join(links) + ")"
                
                parts = line.split('|')
                if len(parts) >= 7:
                    # Remove any existing (See: ...) blocks to avoid duplication
                    note = parts[6].strip()
                    note = re.sub(r'\(See:.*?\)', '', note).strip()
                    
                    if not note or note == "(no note)":
                        parts[6] = f" {link_str} "
                    else:
                        parts[6] = f" {note}{link_str} "
                    line = '|'.join(parts)
        
        new_lines.append(line)

    with open(runs_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    mentions = find_run_mentions()
    update_runs_md(mentions)
    print("Updated RUNS.md with run mentions from blog posts.")
