# 🗳️ Skill: Democracy Protocol (Conflict Resolution)

> **ID:** SKL-GOV-001
> **Owner:** Tier-1 Executive Hub
> **Purpose:** Resolve multi-agent architectural or logic disagreements through weighted consensus.

---

## 🏗️ Voting Mechanics

When two or more agents propose conflicting paths for the same file or module, a **Democracy Session** is triggered.

| Actor | Voting Weight | Responsibility |
| :--- | :--- | :--- |
| **Human Owner** | **Veto Power** | Can override any outcome. |
| **CTS-001 (Chief Technical Supervisor)** | 5 Votes | Final technical integrity. |
| **Department Leads (BE-001, FE-001, SEC-001)**| 3 Votes | Domain-specific authority. |
| **Specialized Agents** | 1 Vote | Technical implementation detail. |

---

## 🔄 Protocol Flow

1. **Detection**: CTS-001 detects a circular or conflicting plan in `memory/global/decisions.md` or during review.
2. **Consultation**: CTS-001 requests short "Advocacy Blurbs" (max 3 lines) from involved agents.
3. **Tally**: Votes are tallied based on the weights above.
4. **Conclusion**: The path with the highest weight is implemented.
5. **Memory Update**: The winning decision is logged with the label `[CONSCENSUS-WIN]`.

---

## 🚫 Use Cases for Voting
- Choice of secondary libraries (e.g., Lucide vs. Heroicons).
- Variable naming conventions in shared folders.
- CSS layout approach (Flex vs. Grid) if not specified in PRD.

## ⛔ Forbidden From Voting (Human Escalation Required)
- Removing security protocols (Socratic Gate).
- Changing core database providers.
- Deleting primary user data.
- Exceeding budget/cost thresholds.

---

## 📢 Standard Communication Format

```markdown
### 🗳️ DEMOCRACY SESSION: [ISSUE_NAME]
- **Proponent A**: [AGENT_ID] - [PATH]
- **Proponent B**: [AGENT_ID] - [PATH]
- **Consensus Result**: [WINNING_PATH]
- **Winning Score**: [N] Votes
- **Justification**: [SUMMARY]
```
