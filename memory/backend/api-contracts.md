# API Contracts: Auth System

## Endpoints

### 1. Register User
- **URL**: `/auth/register`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Success Response**:
  - **Code**: 201 Created
  - **Body**: `{ "id": 1, "email": "user@example.com" }`

### 2. Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Success Response**:
  - **Code**: 200 OK
  - **Body**: `{ "access_token": "...", "token_type": "bearer" }`

### 3. Protected Resource
- **URL**: `/auth/protected`
- **Method**: `GET`
- **Auth Required**: Yes (JWT)
- **Success Response**:
  - **Code**: 200 OK
  - **Body**: `{ "message": "Success", "user": "user@example.com" }`

## Error Format
All errors return a consistent JSON body:
```json
{
  "error": "Error code string",
  "detail": "Human-readable explanation"
}
```
