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
                    # Robust check for Agent ID or agent field
                    if not re.search(r'agent\s*id:', content, re.IGNORECASE) and not re.search(r'agent\s*:', content, re.IGNORECASE):
                        issues.append(f"No ID: {path}")
    return issues

def main():
    root = Path('.')
    print_header("🚀 AGENT-KIT SYSTEM HEALTH CHECK")
    
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
    memory_files = ['memory/global/architecture.md', 'memory/global/conventions.md']
    missing_memory = [m for m in memory_files if not os.path.exists(m)]
    mem_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not missing_memory else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{mem_status}] Global Memory Integrity")
    if missing_memory:
        for m in missing_memory: print(f"  - Missing: {m}")

    print(f"\n{Colors.BOLD}{Colors.GREEN}HEALTH CHECK COMPLETE{Colors.ENDC}")

if __name__ == "__main__":
    main()
