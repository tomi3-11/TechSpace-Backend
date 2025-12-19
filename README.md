# TechSpace Backend API

## PART1: RUNNING THE APP

1️. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Environment variables (.env)
```env
# example template

FLASK_ENV=development
SECRET_KEY=super-secret
JWT_SECRET_KEY=jwt-secret

# Postgres Configs
DATABASE_URL=postgresql://user:yourpassword@localhost:5432/DBNAME

# Mail configs
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com

# Redis Configs
REDIS_URL=redis://localhost:6379/0


```

4. Initialize database
```bash
flask db init
flask db migrate -m "Initial auth tables"
flask db upgrade

```
This creates:
- `users` table
- password reset fields
- role field

5. Run the server
```bash

flask run
```

Server:
```cpp

http://127.0.0.1:5000

```

## PART 2: TESTING ALL AUTH ENDPOINTS (MANDATORY)
Use Postman / curl / Thunder client. etc

### 1. Register User
POST `/api/v1/auth/register/`
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "StrongPass123",
  "password_confirm": "StrongPass123"
}

```
Expected:
```json
{
  "message": "User registered successfully"
}


```

### 2. Login User
POST `/api/v1/auth/login/`
```json

{
  "email": "john@example.com",
  "password": "StrongPass123"
}

```
Expected:
```json

{
  "user": {
    "id": "...",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "avatar_url": "https://ui-avatars.com/..."
  },
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  }
}

```
Save both tokens

### 3. Get Current User
GET `/api/v1/auth/user/`
Headers:
```makefile

Authorization: Bearer ACCESS_TOKEN

```
Return user profile. <br>
Expected:
```json
{
    "id": "...",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "avatar_rule": "https://ui-avatars.com/api/?name=tom5&background=random"
}

```

### 4. Refresh Access Token
POST `/api/v1/auth/token/refresh/` <br>
Headers:
```makefile
Authorization: Bearer REFRESH_TOKEN
```
Body:
```json
{}
```
Expected:
```json
[
    "ACCESS": {
        "..."
    }
]

```

### 5. Logout
POST `/api/v1/auth/logout/` <br>
No headers required
```json

{
    "message": "Logged out successfully"
}
```

Frontend deletes tokens.

### 6. Password Reset (Request)
POST `/api/auth/password/reset/`
```json
{
    "email": "john@example.com"
}

```
Email sent with reset token. <br>

Expected:
```json
{
    "message": "Password reset email sent"
}
```

### 7. Password Reset (Confirm)
POST `/api/v1/auth/password/reset/confirm/`
```json
{
    "token": "RESET_TOKEN",
    "new_password": "NewStrongPass123"
}

```
Password updated. <br>

Expected: 
```json
{
    "message": "Password reset successfully"
}

```

### 8. Login with New Password
Repeat login --> should succeed