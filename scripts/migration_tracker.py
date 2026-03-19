#!/usr/bin/env python3
"""
Migration Progress Tracker

Scans markdown files for migration tracking frontmatter and generates
progress reports for GitHub issues.

Usage:
    python migration_tracker.py [--dir DIR] [--status STATUS] [--format FORMAT]

Examples:
    # Full report
    python migration_tracker.py --dir /path/to/gardenlinux/docs

    # Filter by status
    python migration_tracker.py --dir docs/ --status new,adapt

    # CSV output
    python migration_tracker.py --dir docs/ --format csv
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


def extract_frontmatter(content: str) -> Optional[Dict[str, str]]:
    """Extract YAML frontmatter from markdown content."""
    # Match frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None

    frontmatter_text = match.group(1)
    frontmatter = {}

    # Parse simple key: value pairs
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"\'')

    return frontmatter


def scan_files(directory: Path) -> List[Dict]:
    """Scan all markdown files in directory for migration tracking data."""
    files_data = []

    for md_file in directory.rglob('*.md'):
        # Skip hidden files and node_modules
        if any(part.startswith('.') for part in md_file.parts):
            continue
        if 'node_modules' in md_file.parts:
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = extract_frontmatter(content)
            if not frontmatter:
                continue

            # Check if this file has migration tracking fields
            if 'migration_status' in frontmatter:
                rel_path = md_file.relative_to(directory)
                files_data.append({
                    'path': str(rel_path),
                    'status': frontmatter.get('migration_status', ''),
                    'source': frontmatter.get('migration_source', ''),
                    'issue': frontmatter.get('migration_issue', ''),
                    'stakeholder': frontmatter.get('migration_stakeholder', ''),
                    'approved': frontmatter.get('migration_approved', 'false').lower() == 'true',
                    'title': frontmatter.get('title', md_file.stem)
                })
        except Exception as e:
            print(f"Warning: Could not process {md_file}: {e}", file=sys.stderr)

    return files_data


def filter_by_status(files_data: List[Dict], status_filter: str) -> List[Dict]:
    """Filter files by status."""
    if not status_filter:
        return files_data

    statuses = [s.strip().lower() for s in status_filter.split(',')]
    return [f for f in files_data if f['status'].lower() in statuses]


def generate_markdown_report(files_data: List[Dict]) -> str:
    """Generate markdown report for GitHub issues."""
    if not files_data:
        return "No files with migration tracking found.\n"

    # Count by status
    status_counts = {}
    for f in files_data:
        status = f['status'] or 'unset'
        status_counts[status] = status_counts.get(status, 0) + 1

    # Count approved
    approved_count = sum(1 for f in files_data if f['approved'])

    total = len(files_data)

    # Build report
    report = []
    report.append("## Documentation Migration Progress\n")
    report.append(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Summary table
    report.append("### Summary\n")
    report.append("| Status | Count | Percentage |")
    report.append("|--------|-------|------------|")

    status_emoji = {
        'done': '✅',
        'new': '🆕',
        'adapt': '🔄',
        'merge': '🔀',
        'unset': '❓'
    }

    for status in ['done', 'new', 'adapt', 'merge', 'unset']:
        count = status_counts.get(status, 0)
        percentage = round((count / total * 100)) if total > 0 else 0
        emoji = status_emoji.get(status, '•')
        report.append(f"| {emoji} {status} | {count} | {percentage}% |")

    report.append(f"\n**Approved:** {approved_count}/{total} ({round(approved_count/total*100) if total > 0 else 0}%)\n")

    # Group by status
    for status in ['new', 'adapt', 'merge', 'done', 'unset']:
        status_files = [f for f in files_data if (f['status'] or 'unset') == status]
        if not status_files:
            continue

        emoji = status_emoji.get(status, '•')
        report.append(f"### {emoji} {status.title()} ({len(status_files)} files)\n")

        # Table header
        if status == 'merge':
            report.append("| Done | Approved | File | Sources | Issue | Stakeholder |")
            report.append("|------|----------|------|---------|-------|-------------|")
        elif status in ['adapt', 'new']:
            report.append("| Done | Approved | File | Source | Issue | Stakeholder |")
            report.append("|------|----------|------|--------|-------|-------------|")
        else:
            report.append("| Done | Approved | File | Issue | Stakeholder |")
            report.append("|------|----------|------|-------|-------------|")

        for f in sorted(status_files, key=lambda x: x['path']):
            path = f['path']
            issue = f['issue'] if f['issue'] else '-'
            stakeholder = f['stakeholder'] if f['stakeholder'] else '-'

            # Checkbox for done status
            done_checkbox = '✅' if status == 'done' else '❌'
            # Checkbox for approved
            approved_checkbox = '✅' if f['approved'] else '❌'

            if status == 'merge':
                sources = f['source'].replace(',', ', ') if f['source'] else '-'
                report.append(f"| {done_checkbox} | {approved_checkbox} | `{path}` | {sources} | {issue} | {stakeholder} |")
            elif status in ['adapt', 'new']:
                source = f['source'] if f['source'] else '-'
                report.append(f"| {done_checkbox} | {approved_checkbox} | `{path}` | {source} | {issue} | {stakeholder} |")
            else:
                report.append(f"| {done_checkbox} | {approved_checkbox} | `{path}` | {issue} | {stakeholder} |")

        report.append("")  # Empty line

    return '\n'.join(report)


def generate_csv_report(files_data: List[Dict]) -> str:
    """Generate CSV report."""
    if not files_data:
        return "path,status,source,issue,stakeholder,approved\n"

    lines = ["path,status,source,issue,stakeholder,approved"]

    for f in sorted(files_data, key=lambda x: x['path']):
        approved_str = 'true' if f['approved'] else 'false'
        lines.append(f'"{f["path"]}",{f["status"]},"{f["source"]}","{f["issue"]}","{f["stakeholder"]}",{approved_str}')

    return '\n'.join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Track documentation migration progress from frontmatter fields'
    )
    parser.add_argument(
        '--dir',
        type=Path,
        default=Path('.'),
        help='Directory to scan for markdown files (default: current directory)'
    )
    parser.add_argument(
        '--status',
        type=str,
        help='Filter by status (comma-separated): new,adapt,merge,done'
    )
    parser.add_argument(
        '--format',
        choices=['markdown', 'csv'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    args = parser.parse_args()

    # Resolve to absolute path
    args.dir = args.dir.resolve()

    # Validate directory
    if not args.dir.exists():
        print(f"Error: Directory not found: {args.dir}", file=sys.stderr)
        sys.exit(1)

    # Scan files
    print(f"Scanning {args.dir}...", file=sys.stderr)
    files_data = scan_files(args.dir)
    print(f"Found {len(files_data)} files with migration tracking", file=sys.stderr)

    # Filter if needed
    if args.status:
        files_data = filter_by_status(files_data, args.status)
        print(f"Filtered to {len(files_data)} files with status: {args.status}", file=sys.stderr)

    # Generate report
    if args.format == 'csv':
        report = generate_csv_report(files_data)
    else:
        report = generate_markdown_report(files_data)

    print(report)


if __name__ == '__main__':
    main()
