# Create Workflow

> Build new features following the project plan.

## Trigger
- Task assigned from project plan
- New feature ticket

## Agent Sequence

### Step 1: Task Assignment & Analysis
**Agent:** SFS-001 (Senior Full Stack) -> Assigned department agent
- SFS-001 gives the command and specific prompts for the task
- Department agent reads task requirements
- Load relevant memory files
- Load relevant skills
- Create implementation plan

**Output:** Structured implementation plan (JSON)

### Step 2: Implementation
**Agent:** Assigned department agent(s)
- Write code following conventions
- Follow design system / API contracts
- Stay within file permission boundaries
- Log all file changes

**Rules:**
- Frontend agents → Only modify `src/frontend/`, `src/components/`, etc.
- Backend agents → Only modify `src/backend/`, `src/api/`, etc.
- Database agents → Only modify `src/models/`, `migrations/`, etc.

### Step 3: Self-Review
**Agent:** Same agent performs self-check
- Run through checklist from agent definition
- Verify skill requirements met
- Check for anti-patterns

### Step 4: Code Review
**Agent:** QA-001 (Code Review)
- Review code quality and correctness
- Check convention adherence
- Flag security concerns
- Suggest improvements

**Gate:** 
- If Complexity is **S** and Code Review (Step 4) is approved → **Fast-Track** to Step 7 (Memory Update).
- If Complexity is **M/L/XL** → QA-001 approval leads to Step 5.

### Step 5: Senior Review
**Agent:** SFS-001 (Senior Full Stack)
- Review code and implementation plan for cross-stack consistency
- Ensure all SFS commands were followed
- Provide final feedback before CTS sign-off

**Gate:** SFS-001 approves

### Step 6: CTS Approval
**Agent:** CTS-001 (Chief Technical Supervisor)
- Final review of changes
- Verify no permission violations
- Approve or request changes

**Gate:** CTS-001 approves

### Step 7: Memory Update
**Agent:** MM-001 (Memory Manager)
- Update relevant department memory
- Update component registry / API contracts
- Log decision if any were made

## Memory Updates
- Department memory updated with new patterns/components
- API contracts updated if new endpoints
- Component registry updated if new components

## Failure Handling
- If code review fails → Return to Step 2 with feedback
- If CTS rejects → Return to Step 2 with CTS guidance
- If blocked by dependency → Flag to SP-001 for re-sequencing
