#!/usr/bin/env python3
"""
Generate static HTML pages for authentication system.
"""

from pathlib import Path
import re

ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = ROOT / "site" / "templates"
AUTH_PAGES = [
    "auth-login.html",
    "auth-register.html",
    "auth-forgot-password.html",
    "auth-change-password.html",
    "auth-password-reset.html",
    "auth-password-reset-form.html",
    "auth-password-reset-confirm.html",
    "auth-reset-request.html",
    "auth-reset-confirm.html",
    "auth-reset-password.html",
    "auth-logout.html",
    "auth-profile.html",
    "auth-premium-signup.html",
    "auth-premium-required.html",
]

def generate_auth_pages():
    """Generate static HTML for auth pages."""

    for template_file in AUTH_PAGES:
        template_path = TEMPLATE_DIR / template_file

        if not template_path.exists():
            print(f"Skipping {template_file}: file not found")
            continue

        with open(template_path, 'r') as f:
            content = f.read()

        # Remove Jekyll front matter
        front_matter_match = re.match(r"---\n.*?\n---\n", content, re.DOTALL)
        if front_matter_match:
            content = content[front_matter_match.end():]

        # Determine the output filename
        base_name = template_file.replace('.html', '')
        output_file = f"auth-{base_name}.html"

        output_path = ROOT / "docs" / output_file

        with open(output_path, 'w') as f:
            f.write(content)

        print(f"Generated {output_file}")

    print(f"\nGenerated {len(AUTH_PAGES)} auth pages in docs/")

if __name__ == "__main__":
    generate_auth_pages()
