# Authentication & Authorization System

Backend application implementing a custom authentication and authorization system based on Role-Based Access Control (RBAC).

## Technologies

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Passlib (bcrypt)

---

## Features

### Authentication

- User registration
- Login using username/email and password
- JWT token generation
- Logout
- User profile update
- Soft delete (`is_active = False`)
- Password hashing using bcrypt

### Authorization

Custom RBAC implementation:

- Users
- Roles
- Permissions
- User-Role assignments
- Role-Permission assignments

The application does not rely solely on framework-provided authorization mechanisms. Access control is implemented through custom permission validation.

---

## Database Structure

### users

| Column | Description |
|----------|-------------|
| id | User identifier |
| username | Username |
| password_hash | Bcrypt password hash |
| is_active | User active flag |

### roles

| Column | Description |
|----------|-------------|
| id | Role identifier |
| name | Role name |

Example roles:

- ADMIN
- USER

### permissions

| Column | Description |
|----------|-------------|
| id | Permission identifier |
| resource | Resource name |
| action | Allowed action |

Examples:

| Resource | Action |
|-----------|----------|
| DOCUMENT | READ |
| DOCUMENT | UPDATE |
| USER | READ |
| USER | DELETE |

### user_roles

Many-to-many relationship between users and roles.

### role_permissions

Many-to-many relationship between roles and permissions.

---

## RBAC Scheme

```text
User
  |
user_roles
  |
Role
  |
role_permissions
  |
Permission
```

Authorization flow:

1. User authenticates using username and password.
2. JWT token is issued.
3. Token is validated on each request.
4. User roles are loaded.
5. Permissions are loaded through assigned roles.
6. Access to requested resources is validated.

---

## Error Handling

### 401 Unauthorized

Returned when:

- User is not authenticated
- JWT token is invalid
- JWT token is expired
- User account is inactive

Example:

```json
{
  "detail": "Invalid token"
}
```

### 403 Forbidden

Returned when:

- User is authenticated
- User does not have required permission

Example:

```json
{
  "detail": "Forbidden"
}
```

---

## Mock Business Resource

For demonstration purposes, a mock business resource is implemented.

### Documents

Endpoint:

```http
GET /documents
```

Required permission:

```text
DOCUMENT READ
```

Response:

```json
[
  {
    "id": 1,
    "title": "Contract"
  },
  {
    "id": 2,
    "title": "Invoice"
  }
]
```

---

## First Launch

```python
from src.routers.data import router as data_router

import src.models.user
import src.models.role
import src.models.permission
import src.models.associations

app.include_router(data_router)
```

These lines are required to:

- Register SQLAlchemy models
- Create RBAC tables
- Enable test data initialization endpoint

Run the application and execute:

```http
POST /seed
```

---

## Seed Data

The `/seed` endpoint creates:

### Roles

- ADMIN
- USER

### Permissions

```text
DOCUMENT READ
DOCUMENT UPDATE
USER READ
USER DELETE
```

### Test Users

| Username | Password | Role |
|-----------|-----------|------|
| admin@test.com | admin123 | ADMIN |
| user1@test.com | user123 | USER |
| user2@test.com | user123 | USER |

### Role Permissions

#### ADMIN

```text
DOCUMENT READ
DOCUMENT UPDATE
USER READ
USER DELETE
```

#### USER

```text
DOCUMENT READ
```

---

## API Endpoints

### Authentication

#### Register User

```http
POST /users
```

#### Login

```http
POST /auth/login
```

#### Logout

Client-side JWT removal.

---

### Users

#### Get Users

```http
GET /users
```

Requires:

```text
USER READ
```

#### Soft Delete User

```http
DELETE /users/{user_id}
```

Sets:

```text
is_active = false
```

Requires:

```text
USER DELETE
```

---

### Documents

#### Get Documents

```http
GET /documents
```

Requires:

```text
DOCUMENT READ
```

---

## Running the Project

Install dependencies:

Start PostgreSQL.

Run application:

```bash
uvicorn src.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Authorization Example

1. Login using:

```json
{
  "username": "admin@test.com",
  "password": "admin123"
}
```

2. Copy the received JWT token.
3. Authorize in Swagger.
4. Call protected endpoints.
5. Permissions are checked against roles and permissions stored in the database.

---

## Project Goal

The purpose of this project is to demonstrate:

- Custom authentication implementation
- JWT-based user identification
- Role-Based Access Control (RBAC)
- Database-driven authorization
- Soft delete functionality
- Separation of authentication and authorization concerns
