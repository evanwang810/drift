# Contributing to Drift

Thank you for your interest in contributing to the Drift Agent project!

## Overview

Drift is an autonomous AI agent that explores self-improvement through systematic documentation, tool development, and project-based learning. We welcome contributions that help improve the agent's capabilities, documentation, or overall project health.

## How to Contribute

### Code Contributions

1. **Fork the repository**
   - Click the "Fork" button on GitHub
   - Clone your fork: `git clone https://github.com/your-username/drift.git`

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Edit source files only (never generated outputs)
   - Follow the existing code style
   - Add comments for complex logic

4. **Test your changes**
   ```bash
   # Validate Python syntax
   python -m py_compile agent/tools.py
   python -m py_compile site/build.py

   # Build and validate the site
   python site/build.py
   python site/check_site.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Your feature description"
   ```

6. **Push and create a pull request**
   - Push to your fork: `git push origin feature/your-feature-name`
   - Open a pull request on the main repository

### Documentation Contributions

1. **Read the existing documentation** in `docs/`
2. **Update or create documentation files** in `docs/*.md`
3. **Verify the site builds** with the changes
4. **Submit a pull request**

### Reporting Issues

1. **Search for existing issues** first to avoid duplicates
2. **Create a new issue** with:
   - Clear title and description
   - Steps to reproduce (if applicable)
   - Expected behavior
   - Actual behavior
   - Environment details (Python version, OS, etc.)
   - Screenshots or logs (if applicable)

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### Documentation Standards

- Use Markdown for all documentation
- Include examples for complex concepts
- Keep documentation up-to-date
- Cross-reference related documents

### Testing

- Run validation checks before submitting
- Ensure all `check_site.py` validations pass
- Test changes on both local and live sites
- Check for broken links and missing files

### Project Guidelines

- Work on one project at a time
- Follow the "done when" criteria in `PROJECT.md`
- Edit source files, never generated outputs
- Verify changes before committing

## Areas for Contribution

### Core Agent

- **Tool Development**: Add new tools to `agent/tools.py`
- **Context Management**: Improve wake-up prompt and context
- **Memory Management**: Enhance memory persistence

### Documentation

- **Developer Guide**: Improve development workflow documentation
- **User Guide**: Create guides for end users
- **API Documentation**: Document tool interfaces

### Website

- **Content**: Add new blog posts, documentation, or pages
- **Styling**: Improve CSS and responsive design
- **Navigation**: Update site structure and links

### Testing

- **Validation Scripts**: Add new checks to `site/check_site.py`
- **Test Suite**: Create unit tests for tools
- **Documentation Tests**: Verify documentation accuracy

## Code Review Process

1. **Pull Request Review**: We'll review your changes for quality and correctness
2. **Feedback**: We'll provide feedback and suggestions
3. **Revisions**: Address feedback and make changes
4. **Approval**: Once approved, your changes will be merged

## Community Guidelines

- Be respectful and constructive
- Provide clear, actionable feedback
- Acknowledge contributions
- Follow the project's code of conduct

## Recognition

Contributors will be:
- Listed in `docs/CONTRIBUTORS.md` (when created)
- Acknowledged in blog posts and documentation
- Given credit in commit messages

## Getting Started

If you're new to contributing:

1. Read the [Developer Guide](DEVELOPER_GUIDE.md)
2. Explore the codebase and documentation
3. Pick a small, well-defined issue or feature
4. Start with a simple change
5. Ask questions in the issue tracker or open a pull request

## Questions?

If you have questions about contributing:

- **Issues**: Open a GitHub Issue
- **Discussions**: Use GitHub Discussions
- **Pull Requests**: Start with a small contribution

---

Thank you for helping make Drift better!
