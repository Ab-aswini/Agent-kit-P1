# 🧬 Skill: Memory Compression (Vector-Style)

> **ID:** SKL-META-002
> **Owner:** MM-001 (Memory Manager)
> **Purpose:** Prevent context-limit bloating by intelligently summarizing and archiving verbose memory files.

---

## 📐 The "800-Line Rule"
If any file within `memory/**` exceeds 800 lines of markdown:
1. **Fact Extraction**: Scan the file for critical `[DECISION]` or `[CONVENTION]` tags.
2. **Tabular Summary**: Create a "Fact-Tensor" (Markdown Table) at the top of the file.
3. **Garbage Collection**: Remove verbose chat logs, redundant explanations, or minor task iterations.
4. **Archive**: Move the original verbose version to `memory/archives/[folder]/[file].v1.old.md`.

---

## 🧹 Fact-Tensor Format

Every compressed memory file MUST begin with this header:

| Key Fact | Value/Reference | Rationale |
| :--- | :--- | :--- |
| **System Version** | v2.0.4 | Current stable baseline. |
| **Core Architecture** | Iron Well v2.0 | Separation of Planning/Execution. |
| **Auth Strategy** | JWT + Bcrypt | Industrial-pro standard. |

---

## 🛠️ Compression Tooling (MM-001)

- **Audit**: Run `list_dir` with size metadata once per 10 tasks.
- **Shrink**: Use `replace_file_content` to swap verbose block for a summarized table.
- **Log**: Append a summary of what was removed to `memory/global/maintenance.md`.

---

## 🚫 Forbidden From Deletion
- Security threat models.
- Legal/License definitions.
- Executive tier governance rules.
- Human-Owner explicit overrides.
