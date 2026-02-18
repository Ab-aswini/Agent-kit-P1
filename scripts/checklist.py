import sys
import os
import re
import json
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

POINTER_FILENAME = '.agentkit'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")


def load_agentkit_config():
    """Load .agentkit pointer from CWD. Returns (store_path, paths_dict) or (None, None)."""
    pointer_path = Path(POINTER_FILENAME)
    if pointer_path.exists():
        try:
            config = json.loads(pointer_path.read_text(encoding='utf-8'))
            store = config.get('store', '').replace('/', os.sep)
            paths = {}
            for key, val in config.get('paths', {}).items():
                paths[key] = val.replace('/', os.sep)
            return store, paths
        except Exception as e:
            print(f"{Colors.RED}[X] Error reading {POINTER_FILENAME}: {e}{Colors.ENDC}")
    return None, None


def resolve_path(paths, key, fallback):
    if paths and key in paths:
        return paths[key]
    return fallback


def check_legacy_paths(agents_dir):
    print(f"Checking for legacy .agent/ paths in {agents_dir}...")
    legacy_found = []
    if not os.path.exists(agents_dir):
        return legacy_found
    for root, _, files in os.walk(agents_dir):
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
    if not os.path.exists(agents_dir):
        issues.append(f"Agents directory not found: {agents_dir}")
        return issues
    for root, _, files in os.walk(agents_dir):
        for file in files:
            if file.endswith('.md'):
                path_str = os.path.join(root, file)
                with open(path_str, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not re.search(r'agent\s*id:', content, re.IGNORECASE) and \
                       not re.search(r'agent\s*:', content, re.IGNORECASE):
                        issues.append(f"No ID: {path_str}")
    return issues


def verify_core_components(store_path):
    print("Verifying core framework components...")
    components = {
        'manifest.json': 'Fleet Manifest',
        os.path.join('.agent-os', 'rules', 'protocol-socratic-gate.md'): 'Socratic Gate Protocol',
        os.path.join('.agent-os', 'configs', 'base-config.json'): 'Agent Base Config',
        os.path.join('.agent-os', 'skills', 'democracy-protocol.skill.md'): 'Democracy Protocol',
        os.path.join('.agent-os', 'skills', 'memory-compression.skill.md'): 'Memory Compression Skill',
        os.path.join('scripts', 'security_chaos_test.py'): 'Security Chaos Test',
        os.path.join('scripts', 'sync_api_contracts.py'): 'API Contract Sync Bridge',
        'PROJECT_STATUS.md': 'Project Status Document',
        'METADATA.md': 'SEO Metadata',
    }
    missing = []
    for rel_path, name in components.items():
        full = os.path.join(store_path, rel_path) if store_path else rel_path
        if not os.path.exists(full):
            missing.append(f"Missing: {name} ({rel_path})")
    return missing


def main():
    print_header("🚀 AGENT-KIT SYSTEM HEALTH CHECK v2.0")

    store_path, paths = load_agentkit_config()

    if store_path:
        print(f"{Colors.GREEN}[OK]{Colors.ENDC} Isolated store detected: {store_path}")
    else:
        if os.path.exists('.agent-os'):
            print(f"{Colors.YELLOW}[WARN]{Colors.ENDC} Legacy install (files in project root).")
            print(f"       Run: npx @ab_aswini/agent-kit-p1 clean && npx @ab_aswini/agent-kit-p1 init")
            store_path = '.'
            paths = {
                'agents': os.path.join('.agent-os', 'agents'),
                'rules': os.path.join('.agent-os', 'rules'),
                'memory': 'memory',
                'scripts': 'scripts',
                'docs': 'docs',
            }
        else:
            print(f"{Colors.RED}[FAIL]{Colors.ENDC} No .agentkit pointer and no legacy install found.")
            print(f"       Run: npx @ab_aswini/agent-kit-p1 init")
            sys.exit(1)

    agents_dir = resolve_path(paths, 'agents', os.path.join('.agent-os', 'agents'))
    memory_dir = resolve_path(paths, 'memory', 'memory')

    # 1. Path Integrity
    legacy = check_legacy_paths(agents_dir)
    path_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not legacy else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{path_status}] Path Integrity (No legacy .agent/ references)")
    if legacy:
        for p in legacy: print(f"  - {p}")

    # 2. Agent Health
    agent_issues = verify_agent_structure(agents_dir)
    agent_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not agent_issues else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{agent_status}] Agent Structure (IDs and Context)")
    if agent_issues:
        for i in agent_issues: print(f"  - {i}")

    # 3. Memory Status
    memory_files = [
        os.path.join(memory_dir, 'global', 'architecture.md'),
        os.path.join(memory_dir, 'global', 'conventions.md'),
        os.path.join(memory_dir, 'global', 'decisions.md'),
        os.path.join(memory_dir, 'global', 'project-overview.md'),
    ]
    missing_memory = [m for m in memory_files if not os.path.exists(m)]
    mem_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not missing_memory else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{mem_status}] Global Memory Integrity ({len(memory_files)} files)")
    if missing_memory:
        for m in missing_memory: print(f"  - Missing: {m}")

    # 4. Core Components
    missing_components = verify_core_components(store_path)
    comp_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not missing_components else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{comp_status}] Core Framework Components (Phase 2/3)")
    if missing_components:
        for c in missing_components: print(f"  - {c}")

    # 5. Agent Count
    agent_count = 0
    if os.path.exists(agents_dir):
        for root_dir, _, files in os.walk(agents_dir):
            agent_count += sum(1 for f in files if f.endswith('.agent.md'))
    count_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if agent_count == 53 else f"{Colors.YELLOW}WARN{Colors.ENDC}"
    print(f"[{count_status}] Agent Fleet Count: {agent_count}/53")

    # 6. Footprint Check
    project_root_leaks = ['.agent-os', 'memory', 'scripts', 'docs', 'manifest.json', 'METADATA.md', 'PROJECT_STATUS.md']
    leaks_found = [lp for lp in project_root_leaks if os.path.exists(lp)] if store_path != '.' else []
    leak_status = f"{Colors.GREEN}PASS{Colors.ENDC}" if not leaks_found else f"{Colors.RED}FAIL{Colors.ENDC}"
    print(f"[{leak_status}] Zero-Footprint (no agent files in project root)")
    if leaks_found:
        for lf in leaks_found: print(f"  - Leaked: {lf}")
        print(f"  Run: npx @ab_aswini/agent-kit-p1 clean")

    print(f"\n{Colors.BOLD}{Colors.GREEN}HEALTH CHECK COMPLETE{Colors.ENDC}")


if __name__ == "__main__":
    main()
