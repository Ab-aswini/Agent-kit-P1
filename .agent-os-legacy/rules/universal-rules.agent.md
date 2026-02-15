# Universal Agent Rules (P0)

> **"The AI-OS requires discipline. Rules are not suggestions; they are standard operating procedures."**

## 🔴 THE SOCRATIC GATE (STEP 1)

Before writing ONE line of code for any complex task, you MUST perform a clarity check. 

**Protocol:**
1.  **Stop**: Do not jump to implementation.
2.  **Analyze**: Is the request 100% clear? 
3.  **Ask**: Present the user with exactly 3 (no more, no less) high-value strategic questions.

> 🔴 **VIOLATION:** Implementing a feature without a Socratic check for complexity level 'L' or higher.

---

## 🏗️ 2-PHASE ORCHESTRATION

All complex work follows this flow:

### PHASE 1: PLANNING
-   **Output**: Create/update `docs/PLAN.md`.
-   **Banned**: No code files (`.py`, `.js`, `.ts`, etc.) shall be created or modified.
-   **Gate**: Wait for user "Approved" or "LGTM".

### PHASE 2: EXECUTION
-   **Output**: Implementation of the plan.
-   **Validation**: Run `python scripts/checklist.py` after completion.

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
