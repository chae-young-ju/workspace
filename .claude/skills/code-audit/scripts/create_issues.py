#!/usr/bin/env python3
"""
Create GitHub issues from code analysis findings
"""

import json
import sys
import requests
from typing import List, Dict, Any
from pathlib import Path

class IssueCreator:
    def __init__(self, owner: str, repo: str, token: str):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.api_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        self.created_issues = []

    def get_existing_issues(self) -> List[str]:
        """Get list of existing issue titles to avoid duplicates"""
        try:
            response = requests.get(
                f"{self.api_url}/issues?state=all&per_page=100",
                headers=self.headers
            )
            if response.status_code == 200:
                return [issue['title'] for issue in response.json()]
        except Exception as e:
            print(f"Warning: Could not fetch existing issues: {e}")
        return []

    def create_issue(self, finding: Dict[str, Any]) -> bool:
        """Create a single GitHub issue from a finding"""
        existing_titles = self.get_existing_issues()

        # Map finding type to labels
        label_map = {
            'bug': 'bug',
            'security': 'security',
            'enhancement': 'enhancement',
            'documentation': 'documentation'
        }

        finding_type = finding.get('type', 'enhancement')
        severity = finding.get('severity', 'medium')
        labels = [label_map.get(finding_type, 'enhancement')]

        # Add severity label
        if severity == 'critical':
            labels.append('critical')
        elif severity == 'high':
            labels.append('high-priority')

        title = finding.get('title', 'Code issue')

        # Check for duplicates
        if title in existing_titles:
            return False

        file_path = finding.get('file', 'unknown')
        line = finding.get('line', '?')
        description = finding.get('description', '')
        code_snippet = finding.get('code_snippet', '')

        # Build issue body
        body = f"""## 📍 Location
**File:** `{file_path}`
**Line:** {line}

## 📝 Description
{description}

## 💡 Severity
**{severity.upper()}**

## 📄 Code Snippet
\`\`\`
{code_snippet[:200]}
\`\`\`

---
*This issue was automatically created by the code-audit skill*
"""

        issue_data = {
            "title": title,
            "body": body,
            "labels": labels
        }

        try:
            response = requests.post(
                f"{self.api_url}/issues",
                headers=self.headers,
                json=issue_data
            )

            if response.status_code == 201:
                issue = response.json()
                self.created_issues.append({
                    'number': issue['number'],
                    'title': issue['title'],
                    'url': issue['html_url'],
                    'severity': severity,
                    'type': finding_type
                })
                return True
            else:
                print(f"Error creating issue: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error creating issue: {e}")
            return False

    def create_all_issues(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create all issues from findings"""
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_findings = sorted(
            findings,
            key=lambda x: severity_order.get(x.get('severity', 'low'), 4)
        )

        created_count = 0
        skipped_count = 0

        for finding in sorted_findings:
            if self.create_issue(finding):
                created_count += 1
            else:
                skipped_count += 1

        return {
            'created': created_count,
            'skipped': skipped_count,
            'total': len(findings),
            'issues': self.created_issues
        }

def main():
    if len(sys.argv) < 4:
        print("Usage: python create_issues.py <owner/repo> <token> <findings.json>")
        sys.exit(1)

    repo_string = sys.argv[1]
    token = sys.argv[2]
    findings_file = sys.argv[3]

    # Parse owner/repo
    if '/' not in repo_string:
        print("Error: Repository must be in format 'owner/repo'")
        sys.exit(1)

    owner, repo = repo_string.split('/')

    # Load findings
    try:
        with open(findings_file, 'r', encoding='utf-8') as f:
            findings_data = json.load(f)
        findings = findings_data.get('findings', [])
    except Exception as e:
        print(f"Error loading findings: {e}")
        sys.exit(1)

    # Create issues
    creator = IssueCreator(owner, repo, token)
    result = creator.create_all_issues(findings)

    # Output result
    output = {
        'success': True,
        'repository': f"{owner}/{repo}",
        'created_issues': result['created'],
        'skipped_issues': result['skipped'],
        'total_findings': result['total'],
        'issues': result['issues']
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
