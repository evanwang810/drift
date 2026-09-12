#!/usr/bin/env python3
"""Test the gh issue list command with correct flags."""

import subprocess
import os
import json

# Test the gh issue list command with correct flags
cmd = "gh issue list --state open --json number,title,body,state,comments,createdAt"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

print("Command:", cmd)
print(f"Exit code: {result.returncode}")

if result.returncode == 0:
    issues = json.loads(result.stdout)
    print(f"Number of issues: {len(issues)}")
    if issues:
        print(f"\nFirst issue:")
        print(json.dumps(issues[0], indent=2))
else:
    print(f"Stderr: {result.stderr}")
