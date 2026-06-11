---
name: code-audit
description: |
  Analyze project code and automatically create GitHub issues for bugs, security vulnerabilities, and improvements.
  Use this skill whenever you need to audit code quality, identify technical debt, find bugs, spot security issues, or document improvement opportunities. The skill scans all project files, categorizes findings by severity, and creates GitHub issues automatically with appropriate labels and descriptions.
compatibility: GitHub API access required
---

# Code Audit Skill

Automatically analyze a project's codebase and create GitHub issues for any bugs, security concerns, code quality improvements, and documentation gaps.

## How It Works

1. **Scans all project files** — reads Python, JSON, Markdown, PowerShell, and other key files
2. **Analyzes for common issues**:
   - Logic bugs and potential runtime errors
   - Security vulnerabilities (hardcoded secrets, SQL injection risks, XSS, etc.)
   - Code quality problems (dead code, missing error handling, etc.)
   - Documentation gaps and outdated comments
   - Performance inefficiencies
   - Best practice violations
3. **Creates GitHub issues** automatically with:
   - Descriptive title and detailed explanation
   - Severity-based labels (bug, security, enhancement, documentation)
   - Priority estimation in the description
   - Code snippets or file references where applicable
4. **Returns a summary** of all created issues with links

## Prerequisites

- GitHub repository already created (using the GitHub CLI or API)
- GitHub token (personal access token with `repo` scope)
- Repository owner and name (e.g., `username/repo-name`)

## Usage

Invoke this skill when you need to:
- Find and document bugs before shipping code
- Audit code for security vulnerabilities
- Identify technical debt and refactoring opportunities
- Document missing tests or documentation
- Spot performance issues or inefficiencies

## Input Parameters

The skill will ask for:
- **Project path**: The local directory to analyze (e.g., `C:\Users\Admin\Desktop\workspace`)
- **GitHub repo**: Owner/repo format (e.g., `chae-young-ju/workspace`)
- **GitHub token**: Personal access token with repo permissions

## Output

A summary report containing:
- List of created issues (with GitHub URLs)
- Count by category (bugs, security, enhancements, documentation)
- Any analysis notes or skipped files

## Example Output

```
✅ Code Audit Complete

Created Issues (5):
1. [BUG] Missing error handling in generate_brief.py line 42
   https://github.com/chae-young-ju/workspace/issues/1

2. [SECURITY] Potential hardcoded credential in config file
   https://github.com/chae-young-ju/workspace/issues/2

3. [ENHANCEMENT] Add input validation to JSON config parser
   https://github.com/chae-young-ju/workspace/issues/3

Summary:
- Bugs: 2
- Security: 1
- Enhancements: 2
- Documentation: 0
```

## Notes

- The skill scans common code file types (`.py`, `.json`, `.md`, `.ps1`, etc.)
- Each issue is automatically labeled with priority and category
- Issues link directly to the relevant code file or line when possible
- The skill avoids creating duplicate issues by checking existing issues first
- Sensitive information (API keys, credentials) is flagged for manual review
