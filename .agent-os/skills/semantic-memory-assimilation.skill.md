---
name: Semantic Memory Assimilation
description: Teaches the agent how to natively ingest and trust the V3 auto-synced memory files instead of hallucinating project state.
---

# 🧠 Semantic Memory Assimilation (Gemini 3.1 Cognitive Upgrade)

> **Directive**: Do not guess the structure of the user's project. Do not assume file locations. Read the dynamically generated memory.

When analyzing a codebase, you must pull your context directly from the V3 AST-aware sync outputs located in `paths.memory` (`memory/global/`).
**Since you possess a 2M+ token limit**, favor reading the *entirety* of these documents in one go to form a complete mental model of the system's architecture, skipping piecemeal queries.

## 1. Context Acquisition Targets

Before planning any architectural or coding task, check these ground-truth files:

1. `architecture.md`: Contains the physical directory layout, framework detection results, and language-specific Lines of Code (LOC) counts.
2. `api-contracts.md`: Contains exactly which routes (Express, Next.js, FastAPI, etc.) are physically registered in the AST.
3. `dependencies.md`: Contains the exhaustive list of production packages and their exact verified versions from `package.json`, `requirements.txt`, or `Cargo.toml`.

## 2. Hallucination Prevention

- **Never** assume a route exists just because the user asks about it. Verify it against `api-contracts.md`.
- **Never** suggest installing a package before checking `dependencies.md` to see if it (or an equivalent) is already installed.
- **Always** reference the specific framework versions (e.g., "Since `architecture.md` shows Next.js 14, we will use App Router").

## 3. Integration with the Antigravity Baseline

Combine this memory assimilation with the `@Antigravity-Directive.md`:

1. **Read** complete AST memory context massively into your token window.
2. **Formulate** a Tree-of-Thought plan based _only_ on the registered facts.
3. **Yield** execution back to the IDE AI (Cursor/Copilot/Gemini) via MCP.
