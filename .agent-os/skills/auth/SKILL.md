# Authentication & Authorization Skill

> Loaded by: BE-005 (Auth), BE-006 (RBAC) | Version: 1.0

## Password Handling
- Hash with bcrypt (cost >= 12) or argon2; NEVER store plaintext
- NEVER log passwords; implement password complexity rules

## JWT Tokens
- Access tokens: 15-30 min expiry
- Refresh tokens: 7-30 days, rotate on use
- Minimal claims in payload; NEVER put sensitive data in JWT

## Session Management
- HTTP-only, Secure, SameSite cookies
- Implement session invalidation and track active sessions

## Pattern
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

## Anti-Patterns
- Do NOT implement custom crypto
- Do NOT store tokens in localStorage
- Do NOT skip token validation on protected endpoints
- Do NOT use MD5/SHA1 for passwords
- Do NOT send tokens in URL parameters

## Checklist
- [ ] Passwords hashed with bcrypt/argon2
- [ ] JWT expiry is short and reasonable
- [ ] Refresh tokens rotate on use
- [ ] No sensitive data in tokens
- [ ] HTTPS enforced; brute force protection in place
