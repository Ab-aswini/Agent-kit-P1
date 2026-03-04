# Global Conventions (Antigravity Baseline)

## Development Workflow

1.  **Socratic Gate**: Ask 3 questions (Goal Drift, Alternatives, Worst-Case) before starting tasks.
2.  **Semantic Assimilation**: Never guess the project structure. Read `memory/global/architecture.md` and `api-contracts.md` first.
3.  **Hybrid Hand-off**: Provide perfect execution plans. Yield the typing to the IDE AI.

## Coding Standards (2026+)

- **Error Handling**: Use Discriminated Unions and Result Types `type Result<T, E>`. No naked `try/catch`.
- **Boundaries**: Zod schemas for all external inputs and Database queries.
- **Server-First**: In Next.js/Nuxt, prefer Server Components by default. Treat JS as a liability on the client.

## AI Orchestration

- **Agent IDs**: Always use ID in communication (e.g., SFS-001).
- **Tooling**: Prioritize MCP-native tool execution (`query_ui_ux_engine`).
