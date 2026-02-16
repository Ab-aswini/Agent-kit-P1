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
    # 1. Direct Eval/Shell usage
    for root, _, files in os.walk(search_dir):
        if any(x in root for x in ['node_modules', '.git']): continue
        for file in files:
            if file.endswith(('.js', '.py')):
                path = Path(root) / file
                content = path.read_text(encoding='utf-8')
                if "eval(" in content and "json.parse" not in content.lower():
                    findings.append(f"DANGEROUS: 'eval()' usage in {path}")
                if "shell=True" in content:
                    findings.append(f"RISKY: 'shell=True' in {path}")
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
