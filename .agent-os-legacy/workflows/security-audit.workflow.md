# Security Audit Workflow

> Comprehensive security review of the codebase.

## Trigger
- Pre-deployment (mandatory)
- After dependency updates
- Periodic scheduled audits
- After security incident

## Agent Sequence

### Step 1: Dependency Audit
**Agent:** QA-006 (Security Testing)
- Scan all dependencies for known CVEs
- Flag outdated packages
- Check for abandoned dependencies

### Step 2: Code Security Review
**Agent:** RC-001 (Risk & Compliance)
- Run OWASP Top 10 checklist
- Review authentication implementation
- Check authorization boundaries
- Verify input validation

### Step 3: Infrastructure Review
**Agent:** DO-004 (Server Config) + DO-005 (SSL)
- Verify SSL configuration
- Check security headers
- Review CORS settings
- Verify firewall rules

### Step 4: Secret Scanning
**Agent:** RC-001
- Scan for hardcoded secrets
- Verify all secrets in env vars / secrets manager
- Check git history for leaked secrets

### Step 5: Report
**Agent:** RC-001
- Compile findings into security report
- Assign severity levels
- Recommend fixes with priority order

**Output:** Security audit report with findings and remediation plan

### Step 6: CTS Review
**Agent:** CTS-001
- Review audit findings
- Prioritize fixes
- Assign remediation tasks
- Update risk-log.md

## Memory Updates
- `memory/global/risk-log.md` — All findings
- `memory/qa/security-audit.md` — Audit report
- `memory/global/decisions.md` — Security decisions

## Failure Handling
- Critical findings → Block deployment until fixed
- High findings → Must fix before next release
- Medium findings → Scheduled for fix
- Low findings → Added to backlog
