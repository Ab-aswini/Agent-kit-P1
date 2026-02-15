# Coding Conventions

> Last Updated: [DATE]
> Updated By: [AGENT_ID]

## Naming Conventions

### Files & Folders
- Components: `PascalCase.tsx` (e.g., `UserProfile.tsx`)
- Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
- Styles: `kebab-case.css` (e.g., `user-profile.css`)
- Tests: `*.test.ts` or `*.spec.ts`
- Constants: `UPPER_SNAKE_CASE`

### Code
- Variables/Functions: `camelCase`
- Classes/Components: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Database tables: `snake_case`
- API endpoints: `kebab-case`

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

## Error Handling
- Always use try/catch for async operations
- Return structured error objects
- Log errors with context
- Never swallow errors silently

## Documentation
- All public functions have JSDoc/docstrings
- Complex logic has inline comments
- README kept up to date
