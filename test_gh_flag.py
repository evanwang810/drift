#!/usr/bin/env python3
"""Test the gh command to see what flags are supported."""

import subprocess

# Test the gh issue list command
cmd = "gh issue list --state open --json number,title,body,state,comments,createdAt"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

print("Command:", cmd)
print(f"Exit code: {result.returncode}")
print(f"Output: {result.stdout}")
print(f"Stderr: {result.stderr}")
