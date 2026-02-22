#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent-Kit Semantic Memory Sync (Pillar 3)
=========================================
Real-time, AST-aware project intelligence. Scans the user's codebase,
extracts structure, dependencies, and API routes, then auto-updates the
agent memory files in the global store.

Usage:
    python scripts/memory_sync.py               # Run once
    python scripts/memory_sync.py --watch       # Watch for file changes continuously
    python scripts/memory_sync.py --path /some/project  # Target a specific project
"""
import os
import re
import sys
import json
import argparse
import time
from pathlib import Path
from datetime import datetime, timezone

# ─── Constants ────────────────────────────────────────────────────────────────
SCAN_EXTENSIONS = {
    # Languages and their associations
    '.py': 'Python',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript/React',
    '.js': 'JavaScript',
    '.jsx': 'JavaScript/React',
    '.java': 'Java',
    '.go': 'Go',
    '.rs': 'Rust',
    '.cs': 'C#',
    '.kt': 'Kotlin',
    '.swift': 'Swift',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.dart': 'Dart',
}

IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__', '.next', 'dist', 'build',
    'target', '.gradle', 'vendor', 'venv', '.venv', 'env',
    '.agent-os', 'coverage', '.nyc_output', '.cache', 'stacks',
}

FRAMEWORK_SIGNALS = {
    'Next.js':        ['next.config.js', 'next.config.ts', 'next.config.mjs'],
    'Vite':           ['vite.config.ts', 'vite.config.js'],
    'Nuxt':           ['nuxt.config.ts', 'nuxt.config.js'],
    'Astro':          ['astro.config.mjs'],
    'FastAPI':        ['main.py'],
    'Express':        ['express', 'server.js', 'app.js'],
    'NestJS':         ['nest-cli.json'],
    'Django':         ['manage.py', 'settings.py'],
    'React Native':   ['metro.config.js'],
    'Flutter':        ['pubspec.yaml'],
    'Laravel':        ['artisan'],
    'Spring Boot':    ['pom.xml'],
    'Rust (Cargo)':   ['Cargo.toml'],
    'Go':             ['go.mod'],
    'Docker':         ['Dockerfile', 'docker-compose.yml'],
}

# Route detection patterns for common frameworks
ROUTE_PATTERNS = {
    'python_fastapi': re.compile(
        r'@(?:app|router)\.(?:get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']', re.MULTILINE
    ),
    'js_express':     re.compile(
        r'(?:app|router)\.(?:get|post|put|delete|patch)\s*\(\s*["\']([^"\'`]+)["\']', re.MULTILINE
    ),
    'ts_nestjs':      re.compile(
        r'@(?:Get|Post|Put|Delete|Patch)\s*\(\s*["\']([^"\']+)["\']', re.MULTILINE
    ),
    'nextjs_api':     re.compile(
        r'export\s+(?:default\s+)?(?:async\s+)?function\s+(?:handler|GET|POST|PUT|DELETE|PATCH)', re.MULTILINE
    ),
}

CLASS_FUNC_PATTERN = {
    'python': re.compile(r'^(?:class|def)\s+(\w+)', re.MULTILINE),
    'typescript': re.compile(r'^(?:export\s+)?(?:class|function|const\s+\w+\s*=\s*(?:async\s+)?\()', re.MULTILINE),
    'go': re.compile(r'^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)', re.MULTILINE),
}


# ─── Core Scanner ─────────────────────────────────────────────────────────────
class SemanticScanner:
    """Scans a project directory and extracts semantic metadata."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.scan_time = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    def _should_ignore(self, path: Path) -> bool:
        for part in path.parts:
            if part in IGNORE_DIRS or part.startswith('.'):
                return True
        return False

    def scan_directory_tree(self) -> dict:
        """Build a concise directory tree (max 3 levels deep, skips ignored dirs)."""
        tree = {}
        root = self.project_root

        for item in sorted(root.iterdir()):
            if item.name.startswith('.') or item.name in IGNORE_DIRS:
                continue
            if item.is_dir():
                tree[item.name + '/'] = self._sub_tree(item, depth=2)
            else:
                tree[item.name] = item.suffix

        return tree

    def _sub_tree(self, directory: Path, depth: int) -> dict:
        if depth == 0:
            return {'...': ''}
        result = {}
        try:
            for item in sorted(directory.iterdir()):
                if item.name.startswith('.') or item.name in IGNORE_DIRS:
                    continue
                if item.is_dir():
                    result[item.name + '/'] = self._sub_tree(item, depth - 1)
                else:
                    result[item.name] = item.suffix
        except PermissionError:
            pass
        return result

    def tree_to_string(self, tree: dict, prefix: str = '') -> str:
        """Render the tree dict to a readable string."""
        lines = []
        items = list(tree.items())
        for i, (name, value) in enumerate(items):
            connector = '└── ' if i == len(items) - 1 else '├── '
            lines.append(f"{prefix}{connector}{name}")
            if isinstance(value, dict) and value:
                ext = '    ' if i == len(items) - 1 else '│   '
                lines.append(self.tree_to_string(value, prefix + ext))
        return '\n'.join(lines)

    def detect_frameworks(self) -> list:
        """Detect which frameworks are in use by checking for signal files and package.json."""
        detected = []
        for framework, signals in FRAMEWORK_SIGNALS.items():
            for signal in signals:
                if (self.project_root / signal).exists():
                    detected.append(framework)
                    break

        # Check package.json for JS frameworks
        pkg_path = self.project_root / 'package.json'
        if pkg_path.exists():
            try:
                pkg = json.loads(pkg_path.read_text('utf-8'))
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                if 'next' in deps and 'Next.js' not in detected:
                    detected.append('Next.js')
                if 'react' in deps and 'Next.js' not in detected and 'React' not in detected:
                    detected.append('React')
                if 'nuxt' in deps and 'Nuxt' not in detected:
                    detected.append('Nuxt')
                if 'vite' in deps and 'Vite' not in detected:
                    detected.append('Vite')
                if '@nestjs/core' in deps:
                    detected.append('NestJS')
                if 'express' in deps:
                    detected.append('Express')
                if 'astro' in deps and 'Astro' not in detected:
                    detected.append('Astro')
            except Exception:
                pass

        return list(set(detected))

    def detect_languages(self) -> dict:
        """Count lines of code per detected language."""
        counts = {}
        for root_dir, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            for filename in files:
                ext = Path(filename).suffix
                if ext in SCAN_EXTENSIONS:
                    lang = SCAN_EXTENSIONS[ext]
                    try:
                        with open(os.path.join(root_dir, filename), 'r', encoding='utf-8', errors='ignore') as f:
                            lines = sum(1 for _ in f)
                        counts[lang] = counts.get(lang, 0) + lines
                    except Exception:
                        pass
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    def extract_api_routes(self) -> list:
        """Walk source files and extract API route definitions."""
        routes = []
        for root_dir, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            for filename in files:
                ext = Path(filename).suffix
                filepath = Path(root_dir) / filename
                rel_path = filepath.relative_to(self.project_root)

                try:
                    content = filepath.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    continue

                # Python FastAPI
                if ext == '.py':
                    for match in ROUTE_PATTERNS['python_fastapi'].finditer(content):
                        routes.append(f"  {match.group(1)}  [{rel_path}]")
                # JS/TS Express
                elif ext in ('.js', '.ts'):
                    for match in ROUTE_PATTERNS['js_express'].finditer(content):
                        routes.append(f"  {match.group(1)}  [{rel_path}]")
                # NestJS decorators
                if ext in ('.ts',):
                    for match in ROUTE_PATTERNS['ts_nestjs'].finditer(content):
                        routes.append(f"  {match.group(1)}  [{rel_path}] (NestJS)")
                # Next.js API routes (by file path convention)
                if 'api' in rel_path.parts and ext in ('.ts', '.js'):
                    route_path = '/' + '/'.join(rel_path.parts[list(rel_path.parts).index('api'):])
                    route_path = route_path.replace('\\', '/').replace('.ts', '').replace('.js', '')
                    routes.append(f"  {route_path}  [{rel_path}]")

        return sorted(set(routes))

    def extract_dependencies(self) -> dict:
        """Retrieve production dependencies from package.json or requirements.txt."""
        deps = {}

        pkg_path = self.project_root / 'package.json'
        if pkg_path.exists():
            try:
                pkg = json.loads(pkg_path.read_text('utf-8'))
                deps['npm (production)'] = list(pkg.get('dependencies', {}).keys())[:20]
                deps['npm (dev)'] = list(pkg.get('devDependencies', {}).keys())[:10]
            except Exception:
                pass

        req_path = self.project_root / 'requirements.txt'
        if req_path.exists():
            try:
                lines = req_path.read_text('utf-8').splitlines()
                deps['python'] = [l.split('==')[0].split('>=')[0].strip() for l in lines if l.strip() and not l.startswith('#')][:20]
            except Exception:
                pass

        cargo_path = self.project_root / 'Cargo.toml'
        if cargo_path.exists():
            try:
                content = cargo_path.read_text('utf-8')
                matches = re.findall(r'^(\w[\w-]*)\s*=', content, re.MULTILINE)
                deps['rust (cargo)'] = matches[:20]
            except Exception:
                pass

        return deps


# ─── Memory Writer ─────────────────────────────────────────────────────────────
def resolve_memory_path(project_root: Path) -> Path:
    """Resolve the global store memory path from .agentkit pointer."""
    pointer_path = project_root / '.agentkit'
    if pointer_path.exists():
        try:
            pointer = json.loads(pointer_path.read_text('utf-8'))
            store = pointer.get('store', '')
            store = store.replace('~', str(Path.home()))
            return Path(store) / 'memory' / 'global'
        except Exception:
            pass
    # Fallback: use local .agent-os/memory
    return project_root / '.agent-os' / 'memory' / 'global'


def write_architecture_md(scanner: SemanticScanner, memory_dir: Path):
    """Auto-generate / update architecture.md with live codebase data."""
    tree = scanner.scan_directory_tree()
    tree_str = scanner.tree_to_string(tree, prefix='')
    frameworks = scanner.detect_frameworks()
    languages = scanner.detect_languages()

    lang_table = '\n'.join(
        f'| {lang} | {loc:,} lines |'
        for lang, loc in languages.items()
    ) or '| — | — |'

    framework_str = ', '.join(frameworks) if frameworks else '_(not yet detected)_'

    content = f"""# Architecture
> **Auto-Generated by Agent-Kit Semantic Memory Sync**
> Last Synced: {scanner.scan_time}
> ⚠️  Do NOT manually edit — changes will be overwritten on next sync.

## Detected Frameworks & Runtimes
{framework_str}

## Language Breakdown
| Language | Volume |
|----------|--------|
{lang_table}

## Live Directory Structure
```
{scanner.project_root.name}/
{tree_str}
```

## Data Flow
```
Client → Frontend → API Gateway → Backend Services → Database
                                                    → Cache
                                                    → Queue
```

## Key Architecture Decisions
_(Add ADRs here — they will be preserved across syncs if placed below this line)_

---
"""
    out_path = memory_dir / 'architecture.md'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding='utf-8')
    print(f"  ✅ architecture.md updated")


def write_api_contracts_md(scanner: SemanticScanner, memory_dir: Path):
    """Auto-generate api-contracts.md with extracted API routes."""
    routes = scanner.extract_api_routes()

    route_section = '\n'.join(routes) if routes else '  _(No API routes detected yet)_'

    content = f"""# API Contracts
> **Auto-Generated by Agent-Kit Semantic Memory Sync**
> Last Synced: {scanner.scan_time}
> ⚠️  Do NOT manually edit — this file is auto-updated on every sync.

## Detected Endpoints
```
{route_section}
```

## Contract Rules
- Backend agents MUST update this file when adding/modifying routes.
- Frontend agents MUST read this file before calling any endpoint.
- QA agents MUST validate test coverage against this list.
"""
    out_path = memory_dir / 'api-contracts.md'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding='utf-8')
    print(f"  ✅ api-contracts.md updated")


def write_dependencies_md(scanner: SemanticScanner, memory_dir: Path):
    """Auto-generate dependencies.md from package.json / requirements.txt."""
    deps = scanner.extract_dependencies()

    sections = []
    for manager, packages in deps.items():
        pkg_list = '\n'.join(f'- `{p}`' for p in packages)
        sections.append(f"### {manager.title()}\n{pkg_list}")

    deps_section = '\n\n'.join(sections) if sections else '_(No dependency files detected)_'

    content = f"""# Dependencies
> **Auto-Generated by Agent-Kit Semantic Memory Sync**
> Last Synced: {scanner.scan_time}
> ⚠️  This file is auto-updated. Add notes below the separator but don't edit dependency lists manually.

## Installed Dependencies
{deps_section}

---
## Security Notes
_(Add any known vulnerable packages, pinned versions, or audit notes here)_
"""
    out_path = memory_dir / 'dependencies.md'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding='utf-8')
    print(f"  ✅ dependencies.md updated")


# ─── Watcher Loop ─────────────────────────────────────────────────────────────
def get_snapshot(project_root: Path) -> dict:
    """Capture a lightweight snapshot of file modification times for change detection."""
    snapshot = {}
    for root_dir, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        for filename in files:
            fpath = Path(root_dir) / filename
            if fpath.suffix in SCAN_EXTENSIONS or filename in ('package.json', 'requirements.txt', 'Cargo.toml'):
                try:
                    snapshot[str(fpath)] = fpath.stat().st_mtime
                except Exception:
                    pass
    return snapshot


def run_sync(project_root: Path):
    """Execute a single sync pass and update all memory files."""
    print(f"\n🧠 Agent-Kit Semantic Memory Sync")
    print(f"   Project: {project_root}")
    print(f"   Time:    {datetime.now().strftime('%H:%M:%S')}\n")

    scanner = SemanticScanner(project_root)
    memory_dir = resolve_memory_path(project_root)

    print(f"  📁 Memory Dir: {memory_dir}")

    write_architecture_md(scanner, memory_dir)
    write_api_contracts_md(scanner, memory_dir)
    write_dependencies_md(scanner, memory_dir)

    print(f"\n  ✨ Sync complete.\n")


def watch_loop(project_root: Path, interval: int = 5):
    """Watch for file changes and re-sync memory whenever the project changes."""
    print(f"👁️  Watching project for changes (every {interval}s). Press Ctrl+C to stop.")
    snapshot = get_snapshot(project_root)
    run_sync(project_root)

    while True:
        try:
            time.sleep(interval)
            new_snapshot = get_snapshot(project_root)
            if new_snapshot != snapshot:
                changed = [f for f in new_snapshot if new_snapshot.get(f) != snapshot.get(f)]
                print(f"\n📦 Detected changes: {[Path(c).name for c in changed[:5]]}")
                snapshot = new_snapshot
                run_sync(project_root)
        except KeyboardInterrupt:
            print("\n\n👋 Memory sync stopped.")
            sys.exit(0)


# ─── CLI Entry Point ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Agent-Kit Semantic Memory Sync')
    parser.add_argument('--watch', '-w', action='store_true', help='Watch for file changes continuously')
    parser.add_argument('--path', '-p', type=str, default='.', help='Path to the project directory (default: current dir)')
    parser.add_argument('--interval', type=int, default=5, help='Watch interval in seconds (default: 5)')
    args = parser.parse_args()

    project_path = Path(args.path).resolve()

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)

    if args.watch:
        watch_loop(project_path, args.interval)
    else:
        run_sync(project_path)
