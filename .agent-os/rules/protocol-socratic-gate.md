# 👮 Protocol: The Socratic Gate

> **Status**: Mandatory Global Rule
> **Applied to**: ALL Agents
> **Enforced by**: CTS-001 (Chief Technical Supervisor)

---

## 🛑 The 3-Question Rule

BEFORE an agent can perform any destructive action, write core logic, or propose a major change, they MUST answer the following three questions in their internal thinking or output:

1.  **What is the "Goal Drift"?**
    - _Are we solving the original user problem, or have we drifted into over-engineering?_
2.  **What is the simplest "Cheap" alternative?**
    - _Can this be done in 10 lines of code instead of 100? Can we use an existing skill?_
3.  **What is the "Worst-Case Break"?**
    - _If this change fails or loops, what is the impact on target state and cost?_

---

## 🔄 Integration Requirements

- **Planning Phase**: Every `PLAN.md` created by an agent MUST have a "Socratic Gate Validation" section at the end.
- **Merge Authority**: CTS-001 will REJECT any proposal that does not explicitly address these three questions.

---

## 🚫 Anti-Patterns

- 🚫 Answering with generic "I don't know" or "No drift".
- 🚫 Skipping the gate for "simple" tasks (small tasks often cause the most drift).
- 🚫 Ignoring the "Cheap alternative" in favor of the "Cooler" solution.
