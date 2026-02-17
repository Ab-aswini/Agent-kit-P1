#!/usr/bin/env python3
"""
Agent-Kit: Headless Agent Spawning Script
==========================================
Reads an agent's .md file and its context dependencies,
then outputs a ready-to-paste system prompt for AI assistants.

Usage:
  python scripts/spawn_agent.py BE-001        # Spawn a specific agent
  python scripts/spawn_agent.py --list        # List all available agents
  python scripts/spawn_agent.py --list --dept engineering  # Filter by department
"""

import os
import sys
import json
from pathlib import Path

# Fix Windows terminal encoding for emoji/unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

AGENTS_DIR = Path('.agent-os/agents')
RULES_DIR = Path('.agent-os/rules')
MANIFEST = Path('manifest.json')

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ENDC = '\033[0m'


def find_agent_file(agent_id):
    """Search for an agent file matching the given ID."""
    agent_id_lower = agent_id.lower()
    for root, _, files in os.walk(AGENTS_DIR):
        for file in files:
            if file.endswith('.agent.md'):
                filepath = Path(root) / file
                try:
                    content = filepath.read_text(encoding='utf-8')
                    if agent_id.upper() in content or agent_id_lower in content.lower():
                        return filepath, content
                except Exception:
                    pass
    return None, None


def extract_context_files(content):
    """Extract context loading file references from agent content."""
    context_files = []
    in_context = False
    for line in content.split('\n'):
        if 'context loading' in line.lower() or 'context files' in line.lower():
            in_context = True
            continue
        if in_context:
            if line.strip().startswith('#') and 'context' not in line.lower():
                break
            if '.md' in line or '.json' in line:
                # Extract file paths from markdown links or plain text
                import re
                matches = re.findall(r'[\w\-./]+\.(?:md|json)', line)
                context_files.extend(matches)
    return context_files


def load_context(files):
    """Load content from context dependency files."""
    loaded = {}
    for f in files:
        path = Path(f)
        if not path.exists():
            # Try relative to .agent-os
            path = Path('.agent-os') / f
        if not path.exists():
            # Try relative to .agent-os/rules
            path = RULES_DIR / f
        if path.exists():
            try:
                loaded[str(path)] = path.read_text(encoding='utf-8')
            except Exception:
                pass
    return loaded


def list_agents(dept_filter=None):
    """List all available agents organized by department."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'AGENT-KIT: Available Agents'.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

    count = 0
    for dept_path in sorted(AGENTS_DIR.iterdir()):
        if not dept_path.is_dir():
            continue

        dept_name = dept_path.name
        if dept_filter and dept_filter.lower() not in dept_name.lower():
            # Check subdirs too
            has_match = False
            for sub in dept_path.iterdir():
                if sub.is_dir() and dept_filter.lower() in sub.name.lower():
                    has_match = True
                    break
            if not has_match:
                continue

        agent_files = list(dept_path.rglob('*.agent.md'))
        if not agent_files:
            continue

        print(f"{Colors.BOLD}{Colors.GREEN}[DIR] {dept_name.upper()}{Colors.ENDC}")
        for af in sorted(agent_files):
            name = af.stem.replace('.agent', '')
            # Try to extract agent ID from file content
            try:
                content = af.read_text(encoding='utf-8')
                import re
                id_match = re.search(r'(?:agent\s*id|id)\s*:\s*(\S+)', content, re.IGNORECASE)
                agent_id = id_match.group(1) if id_match else '???'
            except Exception:
                agent_id = '???'
            print(f"  {Colors.DIM}├─{Colors.ENDC} {Colors.YELLOW}{agent_id}{Colors.ENDC}  {name}")
            count += 1
        print()

    print(f"{Colors.BOLD}Total: {count} agents{Colors.ENDC}\n")


def spawn_agent(agent_id):
    """Build and output a complete system prompt for the given agent."""
    print(f"\n{Colors.CYAN}[*] Spawning agent: {agent_id}...{Colors.ENDC}")

    filepath, content = find_agent_file(agent_id)
    if not filepath:
        print(f"{Colors.RED}[X] Agent '{agent_id}' not found.{Colors.ENDC}")
        print(f"{Colors.YELLOW}[?] Run: python scripts/spawn_agent.py --list{Colors.ENDC}")
        sys.exit(1)

    print(f"{Colors.GREEN}[OK] Found: {filepath}{Colors.ENDC}")

    # Load universal rules
    universal = ""
    universal_path = RULES_DIR / 'universal-rules.agent.md'
    if universal_path.exists():
        universal = universal_path.read_text(encoding='utf-8')

    # Load Socratic Gate
    socratic = ""
    socratic_path = RULES_DIR / 'protocol-socratic-gate.md'
    if socratic_path.exists():
        socratic = socratic_path.read_text(encoding='utf-8')

    # Extract and load context dependencies
    context_files = extract_context_files(content)
    loaded_context = load_context(context_files)

    # Build the system prompt
    prompt_parts = [
        "=" * 60,
        "SYSTEM PROMPT — AGENT-KIT HEADLESS SPAWN",
        "=" * 60,
        "",
        "## UNIVERSAL RULES (P0)",
        universal,
        "",
        "## SOCRATIC GATE PROTOCOL",
        socratic,
        "",
        "## AGENT DEFINITION",
        content,
    ]

    if loaded_context:
        prompt_parts.append("\n## LOADED CONTEXT DEPENDENCIES")
        for path, ctx in loaded_context.items():
            prompt_parts.append(f"\n### {path}")
            prompt_parts.append(ctx)

    prompt_parts.extend(["", "=" * 60, "END OF SYSTEM PROMPT", "=" * 60])

    full_prompt = "\n".join(prompt_parts)

    # Output
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}READY — Copy the prompt below:{Colors.ENDC}")
    print(f"{Colors.GREEN}{'='*60}{Colors.ENDC}\n")
    print(full_prompt)
    print(f"\n{Colors.DIM}({len(full_prompt)} characters | {len(full_prompt.split())} words){Colors.ENDC}")


def main():
    args = sys.argv[1:]

    if not args:
        print(f"{Colors.YELLOW}Usage:{Colors.ENDC}")
        print(f"  python scripts/spawn_agent.py BE-001        # Spawn agent")
        print(f"  python scripts/spawn_agent.py --list         # List all agents")
        print(f"  python scripts/spawn_agent.py --list --dept backend  # Filter")
        sys.exit(0)

    if '--list' in args:
        dept = None
        if '--dept' in args:
            idx = args.index('--dept')
            if idx + 1 < len(args):
                dept = args[idx + 1]
        list_agents(dept)
    else:
        spawn_agent(args[0])


if __name__ == "__main__":
    main()
