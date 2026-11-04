# Authentication Data Model Design

## Overview

This document describes the data model for the user authentication system to access premium content.

## Data Structure

### 1. Users Data (`docs/users.json`)

Stores user information including credentials and roles.

```json
{
  "users": [
    {
      "id": "user_001",
      "username": "premium_user",
      "email": "user@example.com",
      "password_hash": "$2b$12$...",
      "role": "premium",
      "created_at": "2026-11-04T14:00:00Z",
      "last_login": "2026-11-04T15:00:00Z",
      "is_active": true
    }
  ]
}
```

**Fields:**
- `id`: Unique identifier (UUID)
- `username`: Unique username (3-50 characters)
- `email`: User email (optional, for password reset)
- `password_hash`: Bcrypt hash of password (never store plaintext)
- `role`: Access level - `guest`, `registered`, or `premium`
- `created_at`: Account creation timestamp
- `last_login`: Last successful login timestamp
- `is_active`: Account status (true = active, false = disabled)

### 2. Sessions Data (`docs/sessions.json`)

Tracks active user sessions for authentication.

```json
{
  "sessions": [
    {
      "session_id": "sess_abc123",
      "user_id": "user_001",
      "created_at": "2026-11-04T15:00:00Z",
      "expires_at": "2026-11-05T15:00:00Z",
      "user_agent": "Mozilla/5.0..."
    }
  ]
}
```

**Fields:**
- `session_id`: Unique session identifier (UUID)
- `user_id`: Foreign key to users.json
- `created_at`: Session creation timestamp
- `expires_at`: Session expiration timestamp (24 hours by default)
- `user_agent`: Browser/user agent string (for security logging)

### 3. Password Reset Tokens (`docs/reset_tokens.json`)

Stores one-time password reset tokens.

```json
{
  "tokens": [
    {
      "token": "reset_xyz789",
      "user_id": "user_001",
      "email": "user@example.com",
      "created_at": "2026-11-04T15:00:00Z",
      "expires_at": "2026-11-04T16:00:00Z",
      "used": false
    }
  ]
}
```

**Fields:**
- `token`: One-time reset token
- `user_id`: User ID being reset
- `email`: Email address (to verify ownership)
- `created_at`: Token creation timestamp
- `expires_at`: Token expiration timestamp (1 hour)
- `used`: Token usage status

## Role-Based Access Control

| Role | Access Level | Premium Content Access |
|------|--------------|------------------------|
| guest | No login required | No access |
| registered | Requires login | Limited access |
| premium | Requires login + upgrade | Full access |

## Security Measures

1. **Password Hashing**: Uses bcrypt with cost factor 12 (industry standard)
2. **Session Management**: 24-hour session expiration, secure cookies
3. **Password Resets**: One-time tokens, 1-hour expiration
4. **Rate Limiting**: Prevent brute force attacks
5. **User Agent Tracking**: Log sessions for security auditing
6. **CSRF Protection**: Token-based CSRF protection for forms

## File Locations

- User data: `docs/users.json`
- Session data: `docs/sessions.json`
- Reset tokens: `docs/reset_tokens.json`
- Authentication module: `site/auth.py`
- Registration page: `docs/register.html`
- Login page: `docs/login.html`
- Profile page: `docs/profile.html`

## Implementation Steps

1. ✅ Design authentication data model (this document)
2. Implement `site/auth.py` with password hashing, session management
3. Create registration and login pages
4. Implement password reset functionality
5. Add middleware to protect premium routes
6. Create user profile management
7. Write comprehensive documentation
8. Test with test users
9. Verify all validations pass
