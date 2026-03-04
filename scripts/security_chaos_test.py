import os
import re
import sys
from pathlib import Path

# Mocking Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"\n{Colors.BOLD}{Colors.FAIL}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.FAIL}{'🐒 SECURITY CHAOS MONKEY v1.0'.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.FAIL}{'='*60}{Colors.ENDC}\n")

def check_exposed_secrets(search_dir):
    """Scan for common patterns of hardcoded keys/secrets."""
    print(f"{Colors.OKBLUE}[*] Searching for exposed credentials...{Colors.ENDC}")
    patterns = [
        r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{10,}['\"]",
        r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{15,}",
        r"(?i)sk_live_[a-zA-Z0-9]{24}", # Stripe-like
    ]
    findings = []
    for root, _, files in os.walk(search_dir):
        if any(x in root for x in ['node_modules', '.git', '.gemini']): continue
        for file in files:
            path = Path(root) / file
            try:
                content = path.read_text(encoding='utf-8')
                for pattern in patterns:
                    if re.search(pattern, content):
                        findings.append(f"Exposed Secret in {path}")
            except: pass
    return findings

def check_logic_flaws(search_dir):
    """Look for dangerous coding patterns or missing auth."""
    print(f"{Colors.OKBLUE}[*] Auditing for Dangerous Logic Patterns...{Colors.ENDC}")
    findings = []

    # Files to skip (this scanner, reference docs)
    skip_files = {'security_chaos_test.py'}
    # Directories to skip (includes skill refs — they contain patterns by design)
    skip_dirs = {'node_modules', '.git', '.gemini', 'skills'}

    # Regex: match actual eval( calls, NOT inside strings or comments
    # Matches: eval(something) but NOT: "eval()" or 'eval()' or description text
    eval_pattern = re.compile(
        r'(?<!["\'])(?<!\w)eval\s*\('  # eval( not preceded by quote or word char
    )
    # For JS: also catch new Function( which is equivalent to eval
    func_pattern = re.compile(r'new\s+Function\s*\(')

    for root, _, files in os.walk(search_dir):
        if any(x in root for x in skip_dirs):
            continue
        for file in files:
            if file in skip_files:
                continue
            if not file.endswith(('.js', '.py')):
                continue
            path = Path(root) / file
            try:
                lines = path.read_text(encoding='utf-8').splitlines()
            except Exception:
                continue

            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # Skip comments
                if stripped.startswith('//') or stripped.startswith('#'):
                    continue
                # Skip lines where eval/shell appear only inside string literals
                if stripped.startswith(('description:', '"description"')):
                    continue

                # Check for eval()
                if eval_pattern.search(line):
                    findings.append(f"DANGEROUS: eval() at {path}:{i}")
                # Check for new Function()
                if file.endswith('.js') and func_pattern.search(line):
                    findings.append(f"DANGEROUS: new Function() at {path}:{i}")
                # Check for shell=True
                if 'shell=True' in line and file.endswith('.py'):
                    findings.append(f"RISKY: shell=True at {path}:{i}")

    return findings

def main():
    print_banner()
    root = "."
    
    # Run Scans
    secrets = check_exposed_secrets(root)
    logic = check_logic_flaws(root)
    
    print(f"\n{Colors.BOLD}--- CHAOS REPORT SUMMARY ---{Colors.ENDC}")
    
    if not secrets and not logic:
        print(f"{Colors.OKGREEN}✅ CLEAN SWEEP: No high-severity chaos detected.{Colors.ENDC}")
    else:
        if secrets:
            print(f"{Colors.FAIL}[!] {len(secrets)} CREDENTIAL RISKS FOUND:{Colors.ENDC}")
            for s in secrets: print(f"  - {s}")
        if logic:
            print(f"{Colors.WARNING}[!] {len(logic)} LOGIC ANOMALIES FOUND:{Colors.ENDC}")
            for l in logic: print(f"  - {l}")
            
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}Chaos session terminated normally.{Colors.ENDC}")

if __name__ == "__main__":
    main()
