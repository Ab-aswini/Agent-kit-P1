# Coding Conventions

> Last Updated: [DATE]
> Updated By: [AGENT_ID]

## Naming Conventions & Code Style

### Files & Hierarchy
- **Components**: `PascalCase.tsx` (e.g., `UserProfile.tsx`)
- **Server Actions/Queries**: `camelCase.ts` (e.g., `updateUser.action.ts`)
- **Schemas**: `camelCase.schema.ts` (e.g., `user.schema.ts`)
- **Constants**: `UPPER_SNAKE_CASE`

### Execution Boundaries
- **Variables/Functions**: `camelCase`
- **Classes/Types/Interfaces**: `PascalCase`
- **Database Tables Maps**: `snake_case`

## Modern Application Architecture (2026+)

1. **Server-First by Default**: In meta-frameworks (Next.js), ship zero JavaScript to the client unless interactivity explicitly demands it (use `"use client"` sparingly at the edge).
2. **Strict Type Boundaries**: All inputs crossing the system boundary (API requests, Database reads) MUST be validated against a strict schema (e.g., `Zod`).
3. **Atomic State**: Prefer localized state (Zustand, XState) over massive global contexts (Redux) unless building a highly complex single-page application.

## Code Style
- Max line length: 100 characters
- Indentation: 2 spaces
- Semicolons: [Yes/No — set per project]
- Quotes: [Single/Double — set per project]

## Git Conventions
- Branch naming: `type/description` (e.g., `feat/user-auth`, `fix/login-redirect`)
- Commit messages: `type(scope): description`
  - Types: feat, fix, refactor, test, docs, chore, perf, ci
- PR requires CTS approval

## Anti-Fragile Error Handling (Rust-Patterns)
- Do not use traditional `try/catch` wrappers that throw generic Exceptions.
- Return explicit discriminated unions: `type Result<T, E> = { ok: true, data: T } | { ok: false, error: E }`
- Log all failures with structured context (UserId, Action, Payload).
- Never swallow errors silently; if you must suppress, leave an aggressive comment explaining why.

## Documentation
- All public functions have JSDoc/docstrings
- Complex logic has inline comments
- README kept up to date
