# Security Audit and Hardening Report

**Date:** 2026-10-14
**Scope:** Repository security review of agent/ and site/ directories
**Status:** FINDINGS IDENTIFIED

## Executive Summary

This security audit identified **one critical vulnerability** (shell command injection) and several **medium-risk issues** related to dependency management and environment variable handling. The good news is that XSS protection is properly implemented throughout the site generation code.

## Critical Vulnerabilities

### 1. Shell Command Injection (HIGH)

**Location:** `agent/tools.py`, multiple locations
**Severity:** CRITICAL
**Description:** The `_run()` method and several GitHub tools use `subprocess.run()` with `shell=True`, accepting user input directly into the command string without sanitization.

**Affected Code:**
```python
# Line 159 - _run() method
def _run(self, command: str) -> str:
    """Run a shell command in the repository root. Network is available."""
    self.actions.append(f"ran: {command[:100]}")
    try:
        done = subprocess.run(
            command, shell=True, cwd=self.root, env=self.env,
            capture_output=True, text=True, timeout=BASH_TIMEOUT,
        )
```

**Risk:** If the command parameter is user-supplied input (which it is for the `_run` tool), an attacker could execute arbitrary shell commands by injecting special characters like `;`, `&&`, `|`, `>`, `<`, `&`, `|`, `;`, or backticks.

**Impact:** The agent could be tricked into executing malicious commands, potentially accessing or modifying files outside the repository, stealing credentials, or performing other harmful actions.

**Affected Locations:**
- Line 159: `_run()` method (general shell command execution)
- Line 419: `_gh_list_issues()` - GitHub API calls via shell
- Line 459: `_gh_read_issue()` - GitHub API calls via shell
- Line 502: `_gh_comment_issue()` - GitHub API calls via shell
- Line 526: `_gh_close_issue()` - GitHub API calls via shell
- Line 629: `_validate_python()` - Python syntax validation via shell
- Line 657: `_validate_python_syntax()` - Python syntax validation via shell
- Line 3011: Site health check - Python compilation via shell
- Multiple other locations with `shell=True`

**Recommendation:** Refactor all subprocess calls to use `shell=False` and pass arguments as a list instead of a string. Use `shlex.split()` if input is a string that needs parsing.

## Medium-Risk Issues

### 2. Environment Variable Exposure in Subprocess Calls

**Location:** `agent/tools.py`, GitHub tool methods
**Severity:** MEDIUM
**Description:** The `GH_TOKEN` environment variable is passed to subprocess calls via `env={**self.env, "GH_TOKEN": gh_token}`. If subprocess output includes environment variable values, the token could be exposed in logs or captured.

**Affected Code:**
```python
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env={**self.env, "GH_TOKEN": gh_token})
```

**Risk:** If the command output or subprocess captures include environment variables, the GH_TOKEN could be logged or exposed in error messages.

**Recommendation:** Ensure that subprocess output does not include environment variables. Use `env` carefully and avoid logging the env parameter.

### 3. Dependency Vulnerability Check Needed

**Location:** `requirements.txt`
**Severity:** MEDIUM
**Description:** No automated dependency vulnerability scanning is implemented.

**Current Dependencies:**
```
requests
beautifulsoup4
markdown
```

**Risk:** If any of these dependencies have known security vulnerabilities (CVEs), they could be exploited without the team knowing.

**Recommendation:** Implement dependency vulnerability scanning using tools like `safety`, `pip-audit`, or `pip-compile` with a lock file.

### 4. No Input Validation on User-Supplied Paths

**Location:** Various file reading/writing tools
**Severity:** MEDIUM
**Description:** While path resolution is handled by `guard.resolve()` and `guard.writable()`, there's no explicit validation that file paths contain only safe characters.

**Risk:** Theoretically, malicious input could attempt path traversal or other filesystem attacks.

**Recommendation:** The current `guard.resolve()` implementation already prevents path traversal, but adding explicit validation could improve clarity.

## Good Security Practices Identified

### 1. XSS Protection (EXCELLENT)

**Location:** `site/build.py`
**Finding:** All HTML output is properly escaped using `html.escape()`.

**Examples:**
```python
# Line 193
<title>{html.escape(title)}</title>

# Line 216
<h1>{html.escape(p['title'])}</h1>

# Line 228
<a href="{p['slug']}.html"><span class="title">{html.escape(p['title'])}</span></a>

# Lines 393-424: Knowledge base and posts HTML escaping
```

**Impact:** Prevents Cross-Site Scripting attacks by escaping user input before rendering.

### 2. Timeout Management (GOOD)

**Finding:** All subprocess calls have appropriate timeouts.

**Examples:**
- `timeout=BASH_TIMEOUT` (60 seconds) for general shell commands
- `timeout=30` for GitHub API calls
- `timeout=10` for Python syntax validation
- `timeout=15` for web fetches

**Impact:** Prevents denial-of-service attacks and resource exhaustion.

### 3. Path Resolution Protection (GOOD)

**Location:** `engine/guard.py`
**Finding:** The `resolve()` and `writable()` functions properly validate paths and prevent access to protected directories.

**Impact:** Prevents the agent from modifying or reading files in `.git`, `engine/`, and other protected areas.

### 4. No SQL Injection (NOT APPLICABLE)

**Finding:** No SQL queries are used in the codebase.

**Impact:** No SQL injection vulnerabilities exist.

### 5. No Code Injection (EXCELLENT)

**Finding:** No use of `eval()`, `exec()`, or `__import__` for executing code dynamically.

**Impact:** Prevents arbitrary code execution vulnerabilities.

## Recommendations for Remediation

### Immediate Actions (Priority 1)

1. **Fix Shell Command Injection:**
   - Refactor `_run()` to use `shell=False`
   - Convert GitHub tool subprocess calls to use argument lists
   - Use `shlex.split()` for parsing command strings
   - Test all affected tools thoroughly

2. **Dependency Vulnerability Scan:**
   - Run `pip-audit` or `safety check`
   - Consider adding a `requirements-lock.txt` for reproducible builds
   - Set up CI/CD checks for dependency vulnerabilities

### Short-Term Actions (Priority 2)

3. **Environment Variable Handling:**
   - Review subprocess output handling
   - Ensure GH_TOKEN is not logged or exposed
   - Consider using environment variables for subprocess commands where possible

4. **Add Security Headers to Static Files:**
   - Add `Content-Security-Policy` headers to HTML files
   - Add `X-Content-Type-Options: nosniff`
   - Add `X-Frame-Options: DENY` or `SAMEORIGIN`

### Long-Term Actions (Priority 3)

5. **Implement Security Headers in Site Generation:**
   - Add security headers to all generated HTML pages
   - Use a consistent security policy across all pages

6. **Add Security Testing:**
   - Create automated tests for security checks
   - Regular security audits (quarterly)
   - Penetration testing for critical vulnerabilities

## Security Best Practices Implemented

✅ No SQL injection (no SQL queries used)
✅ No code injection (no eval/exec/__import__)
✅ Proper XSS protection (html.escape used throughout)
✅ Path resolution validation (guard module)
✅ Subprocess timeout management
✅ No authentication required for static site (expected behavior)
✅ No hardcoded secrets in codebase

## Security Scoring

| Category | Score | Notes |
|----------|-------|-------|
| Injection Vulnerabilities | 3/10 | Critical shell command injection issue |
| XSS Protection | 10/10 | Excellent, all output properly escaped |
| Input Validation | 8/10 | Good path validation, could improve |
| Dependency Security | 6/10 | No vulnerability scanning implemented |
| Authentication | N/A | Static site, no auth needed |
| **Overall** | **6/10** | Good foundation with critical fix needed |

## Conclusion

The codebase demonstrates **good security fundamentals** with proper XSS protection and path validation. However, the **critical shell command injection vulnerability** must be addressed immediately. The project would score much higher once this is fixed and dependency vulnerability scanning is implemented.

The repository is a **static site generator** with no server-side code, which naturally reduces attack surface. The primary security concern is the agent's ability to execute shell commands with user input.

**Next Steps:**
1. Prioritize fixing shell command injection
2. Add dependency vulnerability scanning
3. Implement security headers in site generation
4. Add automated security testing

---
**Report Generated:** 2026-10-14
**Auditor:** Drift Agent (Run 791)
