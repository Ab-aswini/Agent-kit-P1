# Clean Code Skill

> Loaded by: All development agents | Version: 1.0

## Principles

1. **Single Responsibility** - One reason to change per function/class/module
2. **DRY** - Extract shared logic into reusable functions
3. **KISS** - Simplest correct solution wins
4. **Early Return** - Avoid deep nesting with guard clauses
5. **Meaningful Names** - `userCount` not `n`; `isActive` not `flag`
6. **Small Functions** - Max 20-30 lines, max 3-4 parameters
7. **Error Handling** - Specific exceptions, context in messages, handle at right level

## Code Smells
- Functions over 30 lines
- More than 3 parameters
- Deep nesting (>3 levels)
- Comments explaining "what" instead of "why"
- Duplicated code blocks
- God classes/modules

## Checklist
- [ ] Functions are under 30 lines
- [ ] Names are descriptive and consistent
- [ ] No duplicated logic
- [ ] Error handling is complete
- [ ] No magic numbers (use named constants)
- [ ] Comments explain "why", not "what"
