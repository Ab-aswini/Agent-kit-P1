# React Skill

> Loaded by: Frontend Division agents | Version: 1.0

## Best Practices

### Component Structure
- Use functional components with hooks (no class components)
- Keep components under 200 lines; one component per file
- Co-locate related files (component, styles, tests, types)

### Hooks
- Custom hooks for reusable logic (prefix with `use`)
- `useState` for simple local state; `useReducer` for complex state
- `useEffect` cleanup to prevent memory leaks
- `useMemo`/`useCallback` only when measurably needed

### Performance
- React.lazy for route-level code splitting
- React.memo for expensive pure components
- Avoid inline object/array creation in JSX props
- Use stable keys in lists (never array index)

### Pattern
```tsx
interface UserCardProps {
  name: string;
  email: string;
  onEdit?: () => void;
}

const UserCard: React.FC<UserCardProps> = ({ name, email, onEdit }) => (
  <div className="user-card">
    <h3>{name}</h3>
    <p>{email}</p>
    {onEdit && <button onClick={onEdit}>Edit</button>}
  </div>
);

export default UserCard;
```

## Anti-Patterns
- Do NOT use `any` type
- Do NOT mutate state directly
- Do NOT put business logic in components
- Do NOT use `useEffect` for derived state
- Do NOT create components inside render

## Checklist
- [ ] Component is typed with TypeScript interfaces
- [ ] Props have sensible defaults
- [ ] No `any` types
- [ ] Effects have cleanup functions where needed
- [ ] Component is under 200 lines
- [ ] Error boundaries wrap risky components
