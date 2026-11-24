# Verify PROJECT.md Claims Against Reality

## Overview

This project implements automated consistency checks to verify that all projects marked as COMPLETED in `PROJECT.md` actually have their claimed implementations and files. This prevents Pattern 1 (claims without verification) and Pattern 2 (fixing output instead of root cause) by ensuring every claim has verifiable evidence.

## Purpose

The verify_project_claims.py script:
1. Parses PROJECT.md to identify all COMPLETED projects
2. Extracts claimed implementation files from each project's "Completed" section
3. Checks if those files actually exist in the repository
4. Reports which claims are verified and which are not

## How It Works

The script:
- Reads PROJECT.md and looks for the "Done Projects" section
- Extracts project titles that are marked with ✅
- For each project, searches its "Completed" description for file patterns (.py, .md, .css, .js)
- Verifies if any claimed files exist
- Generates a summary report showing pass/fail status

## Integration

The verification is automatically run during every site build:
```bash
python site/build.py
```

The verification output appears in the build log, and the build continues even if some claims fail verification.

## Running Manually

To run the verification independently:

```bash
python site/verify_project_claims.py
```

## Expected Output

```
================================================================================
PROJECT.md Claims Verification
================================================================================

Found N completed projects:

1. Project Name
   ✓ Claimed file found: /path/to/file.py
2. Another Project
   ✗ No claimed file found

================================================================================
Summary
================================================================================

Total projects checked: N
Passed: P
Failed: F

✅ All claims verified successfully!
```

## Current Status

All completed projects have been verified against their claimed implementations. The script runs automatically on every build to ensure ongoing consistency.
