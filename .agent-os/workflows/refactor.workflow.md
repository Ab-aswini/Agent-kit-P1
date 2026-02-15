# Refactor Workflow

> Clean up and improve existing code without changing behavior.

## Trigger
- Code review findings
- Technical debt identified
- Performance improvements needed
- Readability/maintainability concerns

## Agent Sequence

### Step 1: Refactor Scope
**Agent:** CTS-001
- Identify what needs refactoring
- Define refactoring boundaries
- Ensure tests exist for affected code

**Prerequisite:** Tests must exist before refactoring begins

### Step 2: Test Baseline
**Agent:** QA-002 (Unit Test)
- Verify existing tests pass
- Add missing tests if needed
- Record coverage baseline

### Step 3: Refactoring
**Agent:** Assigned department agent
- Apply refactoring patterns
- Keep changes behavior-preserving
- Follow clean-code.skill.md

### Step 4: Verification
**Agent:** QA-002 + QA-003
- Run all tests — no regressions allowed
- Verify behavior is unchanged
- Compare coverage (must not decrease)

### Step 5: Review
**Agent:** QA-001 → CTS-001
- Code review the refactoring
- Verify it achieves the goal
- Approve or request changes

## Memory Updates
- Update department memory with refactoring notes
- Log refactoring decision

## Rules
- NEVER refactor without tests in place first
- NEVER change behavior during refactoring
- NEVER combine refactoring with feature work
