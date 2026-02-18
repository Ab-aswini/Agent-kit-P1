# Universal Agent Rules (P0)

> **"The AI-OS requires discipline. Rules are not suggestions; they are standard operating procedures."**

---

## 🔒 ISOLATED STORE — MANDATORY FIRST STEP

Agent-Kit v2.0 operates in **strict zero-footprint mode**. All agent infrastructure lives in a **global hidden store** — never in the user's project.

### How It Works

1. **Read `.agentkit`** in the project root (a tiny JSON pointer file).
2. Use `paths.memory`, `paths.docs`, `paths.logs`, `paths.scripts`, `paths.agents`, `paths.rules`, `paths.skills` from `.agentkit` for **ALL** reads and writes.
3. **NEVER create** `.agent-os/`, `memory/`, `docs/`, `scripts/`, `manifest.json`, `METADATA.md`, or `PROJECT_STATUS.md` inside the user's project.
4. Write output code **only** to directories the user explicitly owns (`src/`, `app/`, `lib/`, etc.).
5. Agent logs, plans, memory updates — all go to the paths resolved from `.agentkit`.

### `.agentkit` Pointer Format

```json
{
  "version": "2.0.0",
  "store": "~/.agent-os/projects/<project-hash>",
  "paths": {
    "agents": "~/.agent-os/projects/<hash>/.agent-os/agents",
    "memory": "~/.agent-os/projects/<hash>/memory",
    "docs":   "~/.agent-os/projects/<hash>/docs",
    "scripts":"~/.agent-os/projects/<hash>/scripts",
    "logs":   "~/.agent-os/projects/<hash>/.agent-os/logs",
    "rules":  "~/.agent-os/projects/<hash>/.agent-os/rules",
    "skills": "~/.agent-os/projects/<hash>/.agent-os/skills"
  },
  "project": "/absolute/path/to/user/project"
}
```

> 🔴 **VIOLATION:** Creating any agent infrastructure file or directory in the user's project root.

> If `.agentkit` is missing, tell the user to run: `npx @ab_aswini/agent-kit-p1 init`

### Migration from Legacy Installs

If you find `.agent-os/`, `memory/`, `scripts/`, etc. in the project root, instruct the user:
```bash
npx @ab_aswini/agent-kit-p1 clean   # Remove legacy footprint
npx @ab_aswini/agent-kit-p1 init    # Re-initialize with isolated store
```

---

## 🔴 THE SOCRATIC GATE (STEP 1)

> **Canonical Source**: See [protocol-socratic-gate.md](protocol-socratic-gate.md) for the full 3-question protocol.
> 
> **Summary**: Before writing ANY code for complex tasks, you MUST answer 3 strategic questions about Goal Drift, Cheap Alternatives, and Worst-Case Breaks. **No exceptions.**

> 🔴 **VIOLATION:** Implementing a feature without a Socratic check for complexity level 'L' or higher.

---

## 🏗️ 2-PHASE ORCHESTRATION

All complex work follows this flow:

### PHASE 1: PLANNING
-   **Output**: Create/update `PLAN.md` at the path `paths.docs` from `.agentkit` (e.g. `~/.agent-os/projects/<id>/docs/PLAN.md`).
-   **Banned**: No code files (`.py`, `.js`, `.ts`, etc.) shall be created or modified.
-   **Gate**: Wait for user "Approved" or "LGTM".

### PHASE 2: EXECUTION
-   **Output**: Implementation of the plan — write code to the user's project directories only.
-   **Validation**: Run `python <paths.scripts>/checklist.py` (path from `.agentkit`) after completion.

---

## 🧬 CODE QUALITY STANDARDS (SRP/DRY/KISS)

| Principle | Execution |
| :--- | :--- |
| **SRP** | One function, one mission. If it does two things, split it. |
| **DRY** | Extract repeated logic into utilities. No copy-pasting code blocks. |
| **KISS** | Prefer the simplest solution. Avoid over-engineering frameworks for small tasks. |
| **Naming** | Reveal intent. `is_authorized` > `check_auth`. |

---

## 🎨 INDUSTRIAL-PRO AESTHETICS

-   **Documentation**: High contrast, bold headers, use of GitHub-standard emojis.
-   **Reports**: Use tables for data, mermaid for flows, and checklists for tasks.
-   **Voice**: Professional, concise, action-oriented. Skip the "I'd be happy to..." filler.

---

## 🛠️ TOOLING HINTS

-   **Search**: Use `grep_search` before `view_file` to find context.
-   **Verification**: Always run linting/tests before claiming victory.
-   **Errors**: If a command fails, read the error, explain it, then fix it. Do NOT hide the error.
