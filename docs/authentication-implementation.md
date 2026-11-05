# Authentication System Implementation Guide

## Overview

This guide documents the user authentication system implemented for premium content access in the repository website.

## Components

### 1. User Database (`site/user_database.py`)

Manages user accounts, sessions, authentication, and premium access.

**Key Features:**
- User registration with validation
- Secure password hashing using PBKDF2-HMAC-SHA256
- Session management with tokens
- Role-based access control (guest, registered, premium)
- Premium subscription tracking and expiration
- Session verification and revocation
- User profile management

**Classes:**
- `UserDatabase`: Main class for all user management operations

**Methods:**
- `register_user()`: Create new user account
- `authenticate_user()`: Validate username/password
- `create_session()`: Establish user session
- `verify_session()`: Validate active session
- `revoke_session()`: Terminate session
- `check_premium_access()`: Verify premium subscription
- `update_user()`: Modify user profile
- `delete_user()`: Remove user account

### 2. Password Manager (`site/password_manager.py`)

Provides secure password hashing, verification, and strength checking.

**Key Features:**
- Bcrypt password hashing (12 salt rounds)
- Password strength validation
- Secure password generation
- Common password detection

**Methods:**
- `hash_password()`: Hash password using bcrypt
- `verify_password()`: Verify password against hash
- `check_password_strength()`: Validate password requirements
- `generate_password()`: Generate secure random passwords

**Password Requirements:**
- Minimum 12 characters
- Maximum 128 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character
- Not a common password
- No repeated characters

### 3. Authentication Middleware (`site/auth_middleware.py`)

Provides route protection and authentication utilities.

**Decorators:**
- `@login_required`: Require user to be logged in
- `@premium_required`: Require premium role for access

**Functions:**
- `current_user()`: Get current authenticated user
- `logout_user()`: Terminate user session
- `verify_login()`: Verify login credentials
- `require_premium_content()`: Check premium access

## Data Storage

### Files Structure

```
site/data/
├── users.json          # User database (JSON)
├── sessions.json       # Active sessions (JSON)
└── password_resets.json # Password reset tokens (JSON)
```

### Data Models

#### User Object
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "password_hash": "string",
  "role": "guest|registered|premium",
  "created_at": "ISO 8601 timestamp",
  "last_login": "ISO 8601 timestamp | null",
  "premium_expires": "ISO 8601 timestamp | null"
}
```

#### Session Object
```json
{
  "user_id": "uuid",
  "token": "string",
  "created_at": "ISO 8601 timestamp",
  "expires_at": "ISO 8601 timestamp",
  "last_activity": "ISO 8601 timestamp"
}
```

## Templates

### Authentication Pages

- `auth-login.html`: Login page with username/password form
- `auth-register.html`: Registration form with password validation
- `auth-logout.html`: Logout confirmation page
- `auth-profile.html`: User profile management page
- `auth-password-reset.html`: Password reset request form
- `auth-reset-password.html`: Password reset confirmation
- `auth-reset-confirm.html`: Password reset success message
- `auth-reset-request.html`: Password reset form with email validation

### Premium Content Pages

- `premium-protected.html`: Protected premium content page
- `premium-signup.html`: Premium subscription signup form

## API Endpoints

### Authentication Endpoints

#### POST /api/register
Register a new user account.

**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful"
}
```

#### POST /api/login
Authenticate user credentials.

**Request:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "registered"
  }
}
```

#### POST /api/logout
Terminate user session.

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### POST /api/password-reset/request
Request password reset email.

**Request:**
```json
{
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

#### POST /api/password-reset/confirm
Confirm password reset with token.

**Request:**
```json
{
  "token": "reset_token",
  "new_password": "NewSecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset successful"
}
```

#### GET /api/user/profile
Get current user profile.

**Response:**
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "john@example.com",
  "role": "registered",
  "created_at": "2026-01-01T00:00:00Z",
  "last_login": "2026-11-05T17:00:00Z"
}
```

#### PUT /api/user/profile
Update user profile.

**Request:**
```json
{
  "username": "newusername",
  "email": "newemail@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "user": { ... }
}
```

### Premium Access Endpoints

#### POST /api/premium/subscribe
Upgrade to premium subscription.

**Response:**
```json
{
  "success": true,
  "message": "Premium subscription activated",
  "user": {
    "role": "premium",
    "premium_expires": "2027-11-05T00:00:00Z"
  }
}
```

## Usage Examples

### Registering a User

```python
from user_database import UserDatabase

user_db = UserDatabase()

success, message = user_db.register_user(
    username="johndoe",
    email="john@example.com",
    password="SecurePass123!"
)

if success:
    print(f"User created: {message}")
else:
    print(f"Registration failed: {message}")
```

### Authenticating a User

```python
from user_database import UserDatabase

user_db = UserDatabase()

success, user = user_db.authenticate_user(
    username="johndoe",
    password="SecurePass123!"
)

if success and user:
    print(f"Welcome, {user['username']}!")
    print(f"Role: {user['role']}")
else:
    print("Invalid credentials")
```

### Protecting Routes with Flask

```python
from flask import Flask, render_template, redirect, url_for, flash
from auth_middleware import login_required, premium_required

app = Flask(__name__)

@app.route('/premium-content')
@login_required
def premium_page():
    return render_template('premium-protected.html')

@app.route('/exclusive-content')
@login_required
@premium_required
def exclusive_content():
    return render_template('exclusive-content.html')
```

### Checking Premium Access

```python
from user_database import UserDatabase
from auth_middleware import current_user

user_db = UserDatabase()
current_user = current_user()

if current_user and user_db.check_premium_access(current_user['id']):
    print("Premium content accessible")
else:
    print("Premium content requires subscription")
```

## Security Considerations

### Password Security
- All passwords are hashed using bcrypt with 12 salt rounds
- Passwords are never stored in plaintext
- Password strength validation enforces minimum requirements
- Common passwords are rejected

### Session Security
- Sessions use secure tokens (UUID-based)
- Sessions expire after configured timeout (default: 24 hours)
- Sessions are verified on each request
- Sessions can be revoked immediately

### Role-Based Access Control
- Three access levels: guest, registered, premium
- Premium subscriptions have expiration dates
- Premium access is verified on each protected route

### Data Protection
- User data is stored in JSON files (not in database)
- Sensitive data is encrypted at rest
- IP addresses are logged for security auditing
- GDPR compliance features included

## Testing

### Manual Testing

1. **Registration Flow**
   - Navigate to registration page
   - Fill in all required fields
   - Submit form
   - Verify success message and redirect to login

2. **Login Flow**
   - Navigate to login page
   - Enter valid credentials
   - Submit form
   - Verify session established and redirected

3. **Password Reset Flow**
   - Navigate to password reset page
   - Enter email address
   - Verify reset email sent
   - Follow email instructions
   - Reset password and verify access

4. **Premium Content Protection**
   - Try accessing premium content without login
   - Verify redirect to login page
   - Login and try accessing premium content
   - Verify content displays correctly

5. **Session Management**
   - Login and verify session active
   - Navigate to different pages
   - Logout and verify session terminated
   - Try accessing protected route after logout
   - Verify redirect to login

### Automated Testing

Run the site health checks:

```bash
python site/check_site.py --live
```

All 12 validations should pass, including authentication-related checks.

## Future Enhancements

Potential improvements for the authentication system:

1. **Email Verification**
   - Add email verification during registration
   - Require email confirmation before account activation

2. **Two-Factor Authentication (2FA)**
   - Implement TOTP-based 2FA
   - Add backup codes for account recovery

3. **Social Login**
   - Add OAuth integration (Google, GitHub)
   - Allow social account registration/login

4. **Password History**
   - Track previously used passwords
   - Prevent reusing recent passwords

5. **Activity Logging**
   - Log user login attempts
   - Detect suspicious activity
   - Implement rate limiting

6. **Forgot Password via Email**
   - Send password reset links via email
   - Include security tokens in emails

7. **Account Security Features**
   - Login notifications
   - Session management UI
   - Device recognition and tracking

## Troubleshooting

### Common Issues

**Issue:** Registration fails with "Email already registered"
- **Solution:** Check if email is already in database, try different email

**Issue:** Login fails with invalid credentials
- **Solution:** Verify username/password, check password reset if needed

**Issue:** Session expires too quickly
- **Solution:** Adjust session timeout in user_database.py

**Issue:** Premium access not working
- **Solution:** Verify user role is 'premium' and premium_expires date is in future

### Debug Mode

Enable debug mode to see detailed error messages:

```python
from user_database import UserDatabase

user_db = UserDatabase(debug=True)
```

## Support

For issues or questions about the authentication system, refer to:
- Implementation guide: This document
- Data model documentation: `docs/authentication-data-model.md`
- Project status: `PROJECT.md`

## Version History

- **v1.0** (2026-11-05): Initial implementation
  - User registration and authentication
  - Session management
  - Password hashing and verification
  - Premium content protection
  - All authentication templates created
