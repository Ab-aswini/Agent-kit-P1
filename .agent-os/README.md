# .agent-os — System Root

> This directory IS the AI software company. Your AI IDE reads these files to understand roles, rules, and processes.

## How It Works

1. **You open a task** (e.g., "build user authentication")
2. **Reference the relevant workflow** (e.g., `workflows/create.workflow.md`)
3. **The workflow specifies which agents to activate** in what order
4. **Each agent reads its definition** from `agents/` + relevant `skills/` + `memory/`
5. **Agents produce structured JSON output** following templates in `templates/`
6. **CTS-001 approves all changes** before they are finalized
7. **Memory is updated** to persist decisions and context

## Quick Reference

### Start a new project
→ Read `workflows/plan.workflow.md`

### Build a feature
→ Read `workflows/create.workflow.md`

### Fix a bug
→ Read `workflows/debug.workflow.md`

### Deploy
→ Read `workflows/deploy.workflow.md`

## Directory Map

```
.agent-os/
├── config/                 # System configuration
│   ├── agents.json         # Agent registry (all 43 agents)
│   ├── permissions.json    # Who can write where
│   └── settings.json       # Project settings
├── agents/                 # Agent definitions (instructions for AI)
│   ├── tier-1/             # CTS, Strategy Planner, Risk & Compliance
│   ├── engineering/        # Frontend (8), Backend (10), Database (5)
│   ├── qa/                 # Code Review, Unit/Integration/E2E/Perf/Security Test
│   ├── devops/             # Docker, CI/CD, Deploy, Server, SSL, Monitoring
│   ├── product/            # PRD, Docs, Task Tracking, Timeline
│   └── meta/               # Memory Manager, Permissions, Cost, Loop Detection
├── memory/                 # Persistent project knowledge
│   ├── global/             # Architecture, conventions, decisions, risks
│   ├── frontend/           # Design system, component registry
│   ├── backend/            # API contracts, business rules
│   ├── database/           # Schema documentation
│   ├── devops/             # Deployment runbook
│   ├── qa/                 # Review standards, test coverage
│   └── product/            # Milestones, tasks
├── skills/                 # Shared knowledge modules
│   ├── react.skill.md      # React best practices
│   ├── fastapi.skill.md    # FastAPI best practices
│   ├── auth.skill.md       # Authentication patterns
│   ├── security.skill.md   # Security checklist
│   ├── docker.skill.md     # Docker best practices
│   ├── clean-code.skill.md # Clean code principles
│   └── testing.skill.md    # Testing patterns
├── workflows/              # Step-by-step process definitions
│   ├── plan.workflow.md    # Requirements → Milestones
│   ├── create.workflow.md  # Build new features
│   ├── debug.workflow.md   # Fix bugs systematically
│   ├── enhance.workflow.md # Improve existing features
│   ├── test.workflow.md    # Run test suites
│   ├── deploy.workflow.md  # Ship to production
│   ├── refactor.workflow.md # Clean up code
│   └── security-audit.workflow.md # Security review
├── templates/              # Output format templates
│   ├── task-output.json    # Standard agent output
│   ├── review-output.json  # Code review format
│   ├── approval-output.json # CTS approval format
│   ├── risk-finding.json   # Security finding format
│   └── planning-output.json # Planning output format
└── logs/                   # Audit trail
    └── agent-actions.json  # All agent actions logged
```

## Core Rules

1. Every agent has ONE responsibility
2. No agent has global write permission
3. CTS-001 approves all merges
4. Memory is always updated after changes
5. All outputs use structured JSON format
6. All actions are logged

## Phase 1 Active Agents (15)

| ID | Agent | Department |
|----|-------|------------|
| CTS-001 | Chief Technical Supervisor | Executive |
| SP-001 | Strategy Planner | Executive |
| RC-001 | Risk & Compliance | Executive |
| FE-001 | UI Architect | Frontend |
| FE-002 | Layout Engineer | Frontend |
| FE-003 | Component Builder | Frontend |
| FE-005 | API Integration | Frontend |
| BE-001 | API Architect | Backend |
| BE-002 | Route Builder | Backend |
| BE-003 | Controller Logic | Backend |
| BE-005 | Authentication Engineer | Backend |
| DB-001 | Schema Design | Database |
| QA-001 | Code Review | QA |
| PD-001 | PRD Writer | Product |
| MM-001 | Memory Manager | Meta |
