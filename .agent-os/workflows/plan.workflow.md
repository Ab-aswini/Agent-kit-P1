# Plan Workflow

> Converts requirements into structured, actionable milestones.

## Trigger
- New project initialization
- New feature request
- Major scope change

## Agent Sequence

### Step 0: Socratic Gate (Discovery)
**Agent:** SFS-001 (Senior Full Stack Developer)
**Task:** Analyze the user request for complexity (S/M/L/XL).
- If Complexity > S: SFS-001 MUST ask exactly 3 strategic questions to clarify the vision.
- If Complexity = S: Proceed directly to Step 1.
- Wait for user responses before proceeding.

### Step 1: Requirements Analysis
**Agent:** SFS-001 (Senior Full Stack Developer) -> PD-001 (PRD Writer)
- SFS-001 commands PD-001 to gather and clarify requirements
- PD-001 writes user stories with acceptance criteria
- PD-001 defines scope boundaries

**Gate:** Human Owner reviews and approves PRD

### Step 2: Strategic Planning
**Agent:** SP-001 (Strategy Planner)
- Break PRD into milestones
- Define deliverables per milestone
- Estimate complexity (S/M/L/XL)
- Map dependencies between tasks

**Gate:** SFS-001 reviews plan for cross-stack consistency.

### Step 3: Architecture Review
**Agent:** CTS-001 (Chief Technical Supervisor)
- Validate technical approach
- Define module boundaries
- Choose technology stack
- Update architecture.md

**Gate:** Plan is approved

### Step 4: Risk Assessment
**Agent:** RC-001 (Risk & Compliance)
- Identify risks in the plan
- Flag security considerations
- Note compliance requirements

### Step 5: Memory Update
**Agent:** MM-001 (Memory Manager)
- Update `memory/global/project-overview.md`
- Update `memory/global/architecture.md`
- Create `memory/product/milestones.md`
- Initialize department memory files

## Memory Updates
- `memory/global/project-overview.md` — Project summary
- `memory/global/architecture.md` — Technical architecture
- `memory/global/decisions.md` — Key decisions made
- `memory/product/milestones.md` — Full milestone breakdown

## Failure Handling
- If requirements are unclear → Return to Step 1 with specific questions
- If plan is rejected → SP-001 revises based on CTS feedback
- If risks are critical → Escalate to Human Owner

## Output
Structured project plan with milestones, tasks, dependencies, and timeline.
