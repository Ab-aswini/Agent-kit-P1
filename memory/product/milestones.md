# Milestones: FastAPI Auth System

## M-001: Project Setup & User Model
- **T-001**: Initialize FastAPI project structure (BE-001) [S]
- **T-002**: Define User model with SQLAlchemy (DB-001) [S]
- **T-003**: Setup migrations (DB-002) [S]

## M-002: Authentication Logic
- **T-004**: Implement password hashing utility (BE-005) [S]
- **T-005**: Create JWT token generation/validation service (BE-005) [M]
- **T-006**: Create registration endpoint (BE-002/BE-003) [M]
- **T-007**: Create login endpoint (BE-002/BE-003) [M]

## M-003: Middleware & Protection
- **T-008**: Implement Auth middleware for protected routes (BE-007) [M]
- **T-009**: Create protected dummy endpoint for testing (BE-002) [S]

## M-004: Quality & Testing
- **T-010**: Unit tests for hashing & JWT (QA-002) [M]
- **T-011**: Integration tests for Auth endpoints (QA-003) [M]
