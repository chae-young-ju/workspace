#!/usr/bin/env python3
"""
Code analyzer - scans project files for bugs, security issues, and improvements
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any

class CodeAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings = []
        self.file_extensions = {'.py', '.json', '.md', '.ps1', '.txt', '.yaml', '.yml'}

    def analyze(self) -> List[Dict[str, Any]]:
        """Analyze all project files"""
        self._scan_files()
        return self.findings

    def _scan_files(self):
        """Recursively scan all relevant files"""
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.file_extensions:
                self._analyze_file(file_path)

    def _analyze_file(self, file_path: Path):
        """Analyze a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return

        relative_path = file_path.relative_to(self.project_path)

        # Python files
        if file_path.suffix == '.py':
            self._analyze_python(content, relative_path)

        # JSON files
        elif file_path.suffix == '.json':
            self._analyze_json(content, relative_path)

        # All files - security scan
        self._analyze_security(content, relative_path)

        # Markdown files
        if file_path.suffix == '.md':
            self._analyze_markdown(content, relative_path)

    def _analyze_python(self, content: str, file_path: Path):
        """Analyze Python files"""
        lines = content.split('\n')

        # Check for common issues
        for i, line in enumerate(lines, 1):
            # Check for missing error handling
            if 'open(' in line and 'try' not in lines[max(0, i-2):i]:
                self.findings.append({
                    'type': 'bug',
                    'severity': 'medium',
                    'file': str(file_path),
                    'line': i,
                    'title': 'Missing error handling for file operations',
                    'description': f'File operation at line {i} may not have proper error handling. Consider wrapping in try-except block.',
                    'code_snippet': line.strip()[:100]
                })

            # Check for print statements in production code
            if re.match(r'\s*print\(', line) and '__main__' not in content:
                self.findings.append({
                    'type': 'enhancement',
                    'severity': 'low',
                    'file': str(file_path),
                    'line': i,
                    'title': 'Consider using logging instead of print',
                    'description': f'Line {i} uses print(). For production code, consider using the logging module instead.',
                    'code_snippet': line.strip()[:100]
                })

            # Check for hardcoded values
            if any(keyword in line for keyword in ['password=', 'api_key=', 'token=']):
                if '****' not in line and 'example' not in line.lower():
                    self.findings.append({
                        'type': 'security',
                        'severity': 'high',
                        'file': str(file_path),
                        'line': i,
                        'title': 'Potential hardcoded credential',
                        'description': f'Line {i} may contain a hardcoded credential. Move sensitive data to environment variables or secrets management.',
                        'code_snippet': line.strip()[:80]
                    })

        # Check for missing docstrings in functions
        function_pattern = r'^\s*def\s+\w+\s*\('
        for i, line in enumerate(lines):
            if re.match(function_pattern, line):
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if not (next_line.startswith('"""') or next_line.startswith("'''")):
                        # Check if it's a simple getter/setter
                        func_name = re.search(r'def\s+(\w+)', line)
                        if func_name and not any(x in func_name.group(1).lower() for x in ['get', 'set']):
                            self.findings.append({
                                'type': 'enhancement',
                                'severity': 'low',
                                'file': str(file_path),
                                'line': i + 1,
                                'title': 'Missing docstring',
                                'description': f'Function at line {i + 1} is missing a docstring. Add documentation to explain the function\'s purpose.',
                                'code_snippet': line.strip()[:100]
                            })

    def _analyze_json(self, content: str, file_path: Path):
        """Analyze JSON files"""
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            self.findings.append({
                'type': 'bug',
                'severity': 'high',
                'file': str(file_path),
                'line': 1,
                'title': 'Invalid JSON syntax',
                'description': f'JSON file has syntax error: {str(e)}',
                'code_snippet': 'JSON parse error'
            })
            return

        # Check for empty or missing required fields
        if isinstance(data, dict) and len(data) == 0:
            self.findings.append({
                'type': 'enhancement',
                'severity': 'low',
                'file': str(file_path),
                'line': 1,
                'title': 'Empty configuration file',
                'description': f'Configuration file is empty. Add required configuration entries.',
                'code_snippet': '{}'
            })

    def _analyze_security(self, content: str, file_path: Path):
        """Security analysis for all files"""

        # Check for exposed secrets patterns
        secret_patterns = {
            'AWS_KEY': r'(?:AKIA|aws_access_key_id)[\s]*=[\s]*[A-Z0-9]{20}',
            'API_KEY': r'(?:api[_-]?key|apikey)[\s]*=[\s]*[a-zA-Z0-9]{32,}',
            'PASSWORD': r'(?:password|passwd)[\s]*[:=][\s]*["\'](?!.*example)[^"\']{8,}',
            'GH_TOKEN': r'github[_-]?(?:token|pat)[\s]*[:=]',
        }

        for i, line in enumerate(content.split('\n'), 1):
            for pattern_name, pattern in secret_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    # Skip if it's clearly a placeholder or example
                    if any(x in line for x in ['example', 'placeholder', 'XXXXX', 'YOUR_']):
                        continue

                    self.findings.append({
                        'type': 'security',
                        'severity': 'critical',
                        'file': str(file_path),
                        'line': i,
                        'title': f'Potential exposed {pattern_name}',
                        'description': f'Line {i} appears to contain a {pattern_name}. Ensure this is not a real credential. If it is, rotate the credential immediately.',
                        'code_snippet': line.strip()[:80]
                    })

    def _analyze_markdown(self, content: str, file_path: Path):
        """Analyze Markdown files (documentation)"""
        lines = content.split('\n')

        # Check for broken links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for i, line in enumerate(lines, 1):
            matches = re.finditer(link_pattern, line)
            for match in matches:
                url = match.group(2)
                if url.startswith('/') or url.startswith('./'):
                    # Skip relative links that would need filesystem check
                    continue
                if url.startswith('http') and ' ' in url:
                    self.findings.append({
                        'type': 'enhancement',
                        'severity': 'low',
                        'file': str(file_path),
                        'line': i,
                        'title': 'Suspicious URL in markdown',
                        'description': f'Line {i} contains a URL with spaces. Check if the link format is correct.',
                        'code_snippet': line.strip()[:100]
                    })

        # Check for incomplete documentation sections
        if 'TODO' in content or 'FIXME' in content or '[](' in content:
            for i, line in enumerate(lines, 1):
                if 'TODO' in line or 'FIXME' in line:
                    self.findings.append({
                        'type': 'enhancement',
                        'severity': 'medium',
                        'file': str(file_path),
                        'line': i,
                        'title': 'Incomplete documentation (TODO/FIXME)',
                        'description': f'Line {i} contains a TODO or FIXME marker. Complete the documentation.',
                        'code_snippet': line.strip()[:100]
                    })

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyze_code.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    analyzer = CodeAnalyzer(project_path)
    findings = analyzer.analyze()

    # Output as JSON
    output = {
        'total_findings': len(findings),
        'findings': findings,
        'summary': {
            'bugs': len([f for f in findings if f['type'] == 'bug']),
            'security': len([f for f in findings if f['type'] == 'security']),
            'enhancements': len([f for f in findings if f['type'] == 'enhancement']),
            'documentation': len([f for f in findings if f['type'] == 'documentation']),
        }
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
