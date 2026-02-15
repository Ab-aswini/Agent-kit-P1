# FastAPI Skill

> Loaded by: Backend Division agents | Version: 1.0

## Project Structure
```
src/
  api/v1/routes/, schemas/, dependencies/
  core/config.py, security.py
  models/
  services/
  utils/
```

## Best Practices

### Routes
```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return await UserService(db).create(user)
```

### Error Handling
```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"error": "user_not_found", "message": "User with this ID does not exist"}
)
```

### Validation
- Pydantic models for all request/response schemas
- Validate at schema level, not in routes
- Custom validators for business rules

## Anti-Patterns
- Do NOT put business logic in routes
- Do NOT use raw SQL without parameterization
- Do NOT return database models directly (use schemas)
- Do NOT catch broad exceptions silently
- Do NOT hardcode configuration values

## Checklist
- [ ] Routes use proper HTTP methods and status codes
- [ ] Request/response schemas defined
- [ ] Error responses are structured
- [ ] Database sessions properly managed
- [ ] Authentication applied where needed
