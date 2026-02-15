# Architecture

> Last Updated: [DATE]
> Updated By: [AGENT_ID]

## System Architecture
Monolithic FastAPI application using asynchronous request handling and a service-layer pattern for business logic.

## Directory Structure
```
src/
├── backend/
│   ├── main.py (Entry point)
│   ├── auth/ (Auth module)
│   │   ├── services.py (JWT/Hashing)
│   │   ├── routes.py (Register/Login)
│   │   └── middleware.py (JWT Verification)
│   ├── models/ (SQLAlchemy models)
│   └── database/ (Connection setup)
```

## Data Flow
```
Client → Frontend → API Gateway → Backend Services → Database
                                                    → Cache
                                                    → Queue
```

## Key Architecture Decisions

### ADR-001: [Decision Title]
- **Date:** [DATE]
- **Status:** [Proposed | Accepted | Deprecated]
- **Context:** [Why this decision was needed]
- **Decision:** [What was decided]
- **Consequences:** [Trade-offs and implications]

---

| Layer | Technology | Reason |
|-------|-----------|--------|
| Backend Framework | FastAPI | Async, fast performance, Pydantic validation |
| Database | SQLite | Simple, local-first, zero-config for MVP |
| Authentication | JWT | Stateless session management |
| Password Hashing | Argon2 (via Passlib) | State-of-the-art security |

## Module Boundaries
[Which modules exist and their responsibilities]

## API Versioning Strategy
[URL-based, header-based, etc.]

## Authentication Strategy
[JWT, sessions, OAuth, etc.]
