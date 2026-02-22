# 🎯 Agent-Kit Master Hub (hub-logic.md)

> **Role**: Central Intelligence Hub for Agent-Kit  
> **Identity**: The Ultimate IDE Augmentation Arsenal (via MCP)

## 🛡️ Core Directives
1. **The Antigravity Baseline**: All agents run on the cognitive baseline defined in `@Antigravity-Directive.md`.
2. **Hybrid Arsenal (MCP)**: The Hub does not execute code autonomously. It exposes its intelligence, personas, and validation tools via the Model Context Protocol to existing IDE AIs (Cursor, Copilot).
3. **Zero-Footprint**: Agent infrastructure NEVER lives inside the user's project. Only a `.agentkit` pointer file is placed in the project root.
4. **Validation-First**: The Hub provides `checklist.py` and `security_chaos_test.py` as active MCP tools to verify correct implementation.

## 🏗️ Hub Architecture (Global Store)

All infrastructure resides at `~/.agent-os/projects/<project-hash>/`:

- **/.agent-os/agents**: 43+ specialized roles (Executive, Engineering, Meta).
- **/.agent-os/skills**: Reusable capability blocks (Clean Code, Security, DevOps).
- **/.agent-os/rules**: Behavioral constraints (Global P0 Rules).
- **/memory**: User preferences and project context.
- **/.agent-os/workflows**: Pre-defined step sequences for complex tasks.
- **/.agent-os/logs**: Agent action logs.

> ⚠️ **None of these directories exist in the user's project.** They are accessed via the `.agentkit` pointer.

## 🔄 Operations
- **Initialization**: `npx @ab_aswini/agent-kit-p1 init` — sets up global store, writes `.agentkit` pointer.
- **Health Check**: `npx @ab_aswini/agent-kit-p1 doctor` — validates store via pointer.
- **Cleanup**: `npx @ab_aswini/agent-kit-p1 clean` — removes legacy footprint from project root.
- **Task Orchestration**: Senior Full Stack (SFS-001) manages department agents based on this hub.
- **Verification**: Continuous audit via `checklist.py` (resolved from `paths.scripts`).


---

## 🏗️ Specialized Departments

- **Mobile Development** (`engineering/mobile`): Touch-first, battery-conscious, platform-native.
- **Game Development** (`engineering/game`): Mechanics, physics-based animation, cross-platform engines.
- **Security** (`security`): Threat modeling, penetration testing, shift-left audit protocol.
- **Marketing & Growth** (`marketing-growth`): SEO/GEO performance, brand authority.
- **Intelligence** (`intelligence`): Legacy code archaeology, deep research.

## 🎨 Unified UX/UI Protocol (PRO-MAX)

All frontend/design agents MUST utilize the data in `.agent-os/.shared/UI&UX/data/` (resolved via `paths.shared`) for:
- **Animations**: Natural spring physics and distinctive reveal patterns.
- **Colors**: Strict adherence to the Purple Ban and emotion-match palettes.
- **Topological Betrayal**: Avoiding "Safe Harbor" layouts (Standard Hero Split).

## 🔄 Orchestration Logic

1. **Strategy Entry**: `strategy-planner` analyzes and decomposes.
2. **Departmental Execution**: Granular agents follow sequential phases (FE-XXX, BE-XXX).
3. **Security Audit**: Mandatory `security-auditor` gate before production branches.
4. **Verification**: `test-engineer` validates against the "Maestro Auditor" standards.

---
*Built for solo developers who think like companies.*
