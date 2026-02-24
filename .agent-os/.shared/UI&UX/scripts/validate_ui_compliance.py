#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Validator
Scans frontend code (React, Next.js, CSS) for compliance with the Design System.
Flags localized hardcoded color values instead of approved CSS variables.
"""

import sys
import os
import re
import argparse
from pathlib import Path

# Common patterns to detect hardcoded colors
# Matches #FFF, #FFFFFF, rgb(), rgba()
COLOR_PATTERN = re.compile(r'(#([a-fA-F0-9]{3}){1,2}\b|rgba?\([^)]+\))')

# Matches CSS variable declarations (to ignore them)
CSS_VAR_DEF_PATTERN = re.compile(r'--[a-zA-Z0-9-]+:\s*[^;]+;')

# Matches Tailwind arbitrary values like text-[#FF0000]
TAILWIND_ARBITRARY_COLOR = re.compile(r'\b(text|bg|border|fill|stroke)-\[\s*(#([a-fA-F0-9]{3}){1,2}|rgba?\([^)]+\))\s*\]')


def scan_file(filepath):
    """Scans a single file for UI compliance violations."""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return violations

    ext = filepath.suffix.lower()

    if ext == '.css':
        for i, line in enumerate(lines, 1):
            # Ignore lines defining CSS variables
            if CSS_VAR_DEF_PATTERN.search(line):
                continue
            
            matches = COLOR_PATTERN.finditer(line)
            for match in matches:
                color = match.group(0)
                violations.append({
                    'file': str(filepath),
                    'line': i,
                    'issue': f'Hardcoded color found: {color}. Use a CSS variable instead.',
                    'snippet': line.strip()[:100]
                })
                
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        for i, line in enumerate(lines, 1):
            # Check for Tailwind arbitrary colors
            tw_matches = TAILWIND_ARBITRARY_COLOR.finditer(line)
            for match in tw_matches:
                color = match.group(2)
                violations.append({
                    'file': str(filepath),
                    'line': i,
                    'issue': f'Tailwind arbitrary color found: {match.group(0)}. Use a theme token instead.',
                    'snippet': line.strip()[:100]
                })
            
            # General hardcoded hex/rgb in strings (rough heuristic)
            # Only match if inside quotes to reduce false positives in JS
            string_matches = re.finditer(r'["\']([^"\']*?(?:#([a-fA-F0-9]{3}){1,2}|rgba?\([^)]+\))[^"\']*?)["\']', line)
            for match in string_matches:
                # If there's an arbitrary TW match, we likely already caught it, but we can flag it generally
                val = match.group(1)
                
                # Exclude if it's already caught by Tailwind check
                if '[' in val and ']' in val:
                    continue
                    
                violations.append({
                    'file': str(filepath),
                    'line': i,
                    'issue': f'Hardcoded color string found: "{val}". Extract to design system.',
                    'snippet': line.strip()[:100]
                })

    return violations


def main():
    parser = argparse.ArgumentParser(description="Validate UI Code against Design System")
    parser.add_argument("target_dir", help="Directory to scan")
    parser.add_argument("--fail-on-error", action="store_true", help="Exit with non-zero code if violations found")
    
    args = parser.parse_args()
    target = Path(args.target_dir)
    
    if not target.exists() or not target.is_dir():
        print(f"Error: {target} is not a valid directory.")
        sys.exit(1)
        
    print(f"Scanning {target} for UI compliance violations...\n")
    
    all_violations = []
    
    for root, _, files in os.walk(target):
        for file in files:
            path = Path(root) / file
            if path.suffix.lower() in ['.css', '.js', '.jsx', '.ts', '.tsx']:
                all_violations.extend(scan_file(path))
                
    if not all_violations:
        print("✅ UI Compliance Check Passed! No hardcoded colors found.")
        sys.exit(0)
        
    print(f"❌ Found {len(all_violations)} UI compliance violations:\n")
    
    # Group by file
    grouped = {}
    for v in all_violations:
        grouped.setdefault(v['file'], []).append(v)
        
    for file, violations in grouped.items():
        print(f"📄 {file}")
        for v in violations:
            print(f"  Line {v['line']}: {v['issue']}")
            print(f"    Code: {v['snippet']}")
        print()
        
    if args.fail_on_error:
        sys.exit(1)

if __name__ == "__main__":
    main()
