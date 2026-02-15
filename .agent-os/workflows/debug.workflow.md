# Debug Workflow

> Systematically identify and fix bugs.

## Trigger
- Bug report from user
- Error in monitoring/logs
- Test failure

## Agent Sequence

### Step 1: Bug Analysis
**Agent:** CTS-001 (Chief Technical Supervisor)
- Identify which department/module is affected
- Assign to appropriate agent
- Set priority level

### Step 2: Root Cause Analysis
**Agent:** Assigned department agent
- Reproduce the bug
- Trace through code to find root cause
- Document findings

**Output:**
```json
{
  "bug_id": "BUG-XXX",
  "root_cause": "Description of what causes the bug",
  "affected_files": ["path/to/file"],
  "impact": "What this bug affects",
  "proposed_fix": "How to fix it"
}
```

### Step 3: Fix Implementation
**Agent:** Same department agent
- Implement the fix
- Ensure no regressions
- Stay within permission boundaries

### Step 4: Security Check
**Agent:** RC-001 (Risk & Compliance)
- Verify fix doesn't introduce vulnerabilities
- Check if bug was security-related

### Step 5: Test Verification
**Agent:** QA-001 (Code Review) + QA-002 (Unit Test)
- Review the fix
- Write regression test
- Verify existing tests pass

### Step 6: CTS Approval
**Agent:** CTS-001
- Approve fix and merge

### Step 7: Memory Update
- Update department memory with bug details
- Update risk-log.md if security-related
- Add regression test to test suite

## Failure Handling
- If root cause unclear → Escalate to CTS-001 for broader investigation
- If fix causes regressions → Revert and re-analyze
- If security-related → Fast-track through RC-001
