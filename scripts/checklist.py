import sys
import os
import re
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def check_legacy_paths(root_dir):
    print(f"Checking for legacy .agent/ paths in {root_dir}...")
    legacy_found = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    if '.agent/' in f.read():
                        legacy_found.append(file_path)
            except: pass
    return legacy_found

def verify_agent_structure(agents_dir):
    print(f"Verifying agent IDs and context in {agents_dir}...")
    issues = []
    for root, _, files in os.walk(agents_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not re.search(r'agent\s*id:', content, re.IGNORECASE) and not re.search(r'agent\s*:', content, re.IGNORECASE):
                        issues.append(f"No ID: {path}")
    return issues

def verify_core_components():
    """L3 Fix: Verify Phase 2/3 components exist."""
    print("Verifying core framework components...")
    components = {
        'manifest.json': 'Fleet Manifest',
        '.agent-os/rules/protocol-socratic-gate.md': 'Socratic Gate Protocol',
        '.agent-os/configs/base-config.json': 'Agent Base Config',
        '.agent-os/skills/democracy-protocol.skill.md': 'Democracy Protocol',
        '.agent-os/skills/memory-compression.skill.md': 'Memory Compression Skill',
        'scripts/security_chaos_test.py': 'Security Chaos Test',
        'scripts/sync_api_contracts.py': 'API Contract Sync Bridge',
        'PROJECT_STATUS.md': 'Project Status Document',
        'METADATA.md': 'SEO Metadata',
    }
    missing = []
    for path, name in components.items():
        if not os.path.exists(path):
            missing.append(f"Missing: {name} ({path})")
    return missing

def main():
    root = Path('.')
    print_header("🚀 AGENT-KIT SYSTEM HEALTH CHECK v1.1")
    
    # 1. Path Integrity
    legacy = check_legacy_paths('.agent-os')
    path_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not legacy else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{path_status}] Path Integrity (No legacy .agent/ references)")
    if legacy:
        for p in legacy: print(f"  - {p}")

    # 2. Agent Health
    agent_issues = verify_agent_structure('.agent-os/agents')
    agent_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not agent_issues else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{agent_status}] Agent Structure (IDs and Context)")
    if agent_issues:
        for i in agent_issues: print(f"  - {i}")

    # 3. Memory Status
    memory_files = ['memory/global/architecture.md', 'memory/global/conventions.md', 'memory/global/decisions.md', 'memory/global/project-overview.md']
    missing_memory = [m for m in memory_files if not os.path.exists(m)]
    mem_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not missing_memory else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{mem_status}] Global Memory Integrity ({len(memory_files)} files)")
    if missing_memory:
        for m in missing_memory: print(f"  - Missing: {m}")

    # 4. Core Components (NEW - Phase 2/3)
    missing_components = verify_core_components()
    comp_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not missing_components else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{comp_status}] Core Framework Components (Phase 2/3)")
    if missing_components:
        for c in missing_components: print(f"  - {c}")

    # 5. Agent Count
    agent_count = 0
    for root_dir, _, files in os.walk('.agent-os/agents'):
        agent_count += sum(1 for f in files if f.endswith('.agent.md'))
    count_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if agent_count == 53 else f"{Colors.YELLOW}WARN{Colors.ENDC}"
    print(f"[{count_status}] Agent Fleet Count: {agent_count}/53")

    print(f"\n{Colors.BOLD}{Colors.GREEN}HEALTH CHECK COMPLETE{Colors.ENDC}")

if __name__ == "__main__":
    main()
