# PRD: Secure FastAPI User Authentication System

## Overview
A lightweight, secure authentication service built with FastAPI, using JWT tokens for session management and SQLite for data persistence.

## User Stories
- **US-1: User Registration** - As a new user, I want to create an account with email and password so I can access secured endpoints.
- **US-2: User Login** - As a registered user, I want to login with my credentials and receive a JWT token.
- **US-3: Access Protected Routes** - As an authenticated user, I want to use my JWT token to access routes that are hidden from public users.

## Functional Requirements
1. **Registration Endpoint**: `POST /auth/register` (email, password).
2. **Login Endpoint**: `POST /auth/login` (email, password) -> returns access token.
3. **Token Verification**: Middleware to validate JWT in `Authorization: Bearer <token>` header.
4. **Password Hashing**: Use Argon2 or bcrypt for secure storage.
5. **Database**: SQLite with SQLAlchemy ORM.

## Non-Functional Requirements
- **Security**: Passwords must never be stored in plain text.
- **Performance**: Auth check overhead < 50ms.
- **Portability**: All configuration via environment variables.

## Acceptance Criteria
- [ ] Successful registration returns 201 Created.
- [ ] Login with invalid credentials returns 401 Unauthorized.
- [ ] Accessing `/protected` without a token returns 401 Unauthorized.
- [ ] Accessing `/protected` with a valid token returns 200 OK.
