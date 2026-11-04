# Authentication Data Model and Schema

## Overview
This document defines the data structures and schemas for the user authentication system implemented for premium content access.

## Core Components

### 1. User Data Model

```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "password_hash": "string",
  "role": "guest|registered|premium",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp",
  "last_login": "ISO 8601 timestamp | null",
  "preferences": {
    "email_notifications": true,
    "newsletter_subscription": true,
    "privacy_consent": true
  },
  "is_active": true,
  "metadata": {
    "ip_address": "string | null",
    "user_agent": "string | null",
    "registration_source": "string | null"
  }
}
```

**User Fields:**
- `id`: Unique identifier (UUID v4)
- `username`: Unique username (3-50 characters, alphanumeric with underscores)
- `email`: Unique email address (validation required)
- `password_hash`: bcrypt hash of password (never store plaintext passwords)
- `role`: Access level (guest, registered, premium)
- `created_at`: Account creation timestamp
- `updated_at`: Last modification timestamp
- `last_login`: Timestamp of last successful login (null for new accounts)
- `preferences`: User preferences object
  - `email_notifications`: Boolean for email subscription status
  - `newsletter_subscription`: Boolean for newsletter status
  - `privacy_consent`: Boolean for GDPR consent
- `is_active`: Account status (active/inactive)
- `metadata`: Additional tracking information
  - `ip_address`: Registration IP (for security)
  - `user_agent`: Browser/User-Agent string
  - `registration_source`: Where user signed up (direct, newsletter, referral)

### 2. Session Data Model

```json
{
  "session_id": "string",
  "user_id": "uuid",
  "token": "string",
  "created_at": "ISO 8601 timestamp",
  "expires_at": "ISO 8601 timestamp",
  "ip_address": "string",
  "user_agent": "string",
  "last_activity": "ISO 8601 timestamp",
  "is_valid": true
}
```

**Session Fields:**
- `session_id`: Unique session identifier (UUID v4)
- `user_id`: Reference to user object
- `token`: Security token for session validation
- `created_at`: Session creation timestamp
- `expires_at`: Session expiration timestamp (typically 24-48 hours)
- `ip_address`: IP address associated with session
- `user_agent`: Browser/User-Agent string
- `last_activity`: Timestamp of last session activity
- `is_valid`: Current session validity status

### 3. Password Reset Token Model

```json
{
  "token": "string",
  "user_id": "uuid",
  "created_at": "ISO 8601 timestamp",
  "expires_at": "ISO 8601 timestamp",
  "used": false
}
```

**Password Reset Fields:**
- `token`: Unique reset token
- `user_id`: Reference to user object
- `created_at`: Token creation timestamp
- `expires_at`: Token expiration (typically 1 hour)
- `used`: Whether token has been used

### 4. Authentication Token Model

```json
{
  "token": "string",
  "user_id": "uuid",
  "type": "access_token|refresh_token",
  "created_at": "ISO 8601 timestamp",
  "expires_at": "ISO 8601 timestamp",
  "scopes": ["read", "write"]
}
```

**Token Fields:**
- `token`: Unique token string
- `user_id`: Reference to user
- `type`: Token type (access or refresh)
- `created_at`: Token creation timestamp
- `expires_at`: Token expiration
- `scopes`: Token permissions (e.g., read, write, premium_access)

## File Storage Structure

```
data/
├── users.json          # User database (JSON array)
├── sessions.json       # Active sessions (JSON array)
├── password_resets.json# Password reset tokens (JSON array)
└── tokens.json         # Refresh tokens (JSON array)
```

## Security Considerations

### Password Storage
- Use bcrypt with salt rounds (minimum 12)
- Never store plaintext passwords
- Use password strength validation (minimum 12 characters, mixed case, numbers, special chars)
- Implement rate limiting on registration/login

### Session Management
- Sessions expire after 24 hours of inactivity
- Secure session cookies with HTTPOnly and SameSite flags
- Regenerate session ID after authentication
- Track IP address and user agent for security validation

### Token Security
- Use cryptographically secure random token generation
- Short-lived access tokens (15-30 minutes)
- Long-lived refresh tokens (7-30 days)
- Invalidate tokens on logout or session timeout

### Data Protection
- Encrypt sensitive data at rest (password hashes)
- Implement CSRF protection
- Use HTTPS for all authentication endpoints
- Log authentication events for audit trail

## Role-Based Access Control (RBAC)

### Roles and Permissions

| Role   | Access Level                          | Premium Content |
|--------|---------------------------------------|-----------------|
| guest  | No authentication required           | No              |
| registered | Login required, basic access        | No              |
| premium | All registered privileges + premium  | Yes             |

### Premium Content Protection

Premium content is identified by the `premium` attribute in the content metadata. Only users with `role === "premium"` can access this content.

```json
{
  "id": "post-1",
  "title": "Premium Tutorial",
  "content": "...",
  "premium": true,
  "metadata": {
    "access_level": "premium",
    "description": "Advanced content requiring subscription"
  }
}
```

## Data Validation Rules

### User Validation
- Username: 3-50 characters, alphanumeric + underscore only
- Email: Valid email format, unique across all users
- Password: Minimum 12 characters, mixed case, numbers, special chars
- Role: Only valid values: guest, registered, premium

### Session Validation
- Session ID: UUID format
- User ID: Valid UUID and existing user
- Token: Non-empty string
- Timestamps: Valid ISO 8601 format
- IP Address: Valid IPv4 or IPv6 format

## Migration Strategy

### Initial State
- Empty users.json
- Empty sessions.json
- Empty password_resets.json
- Empty tokens.json

### Migration from Guest to Registered
1. Users start with `role: "guest"`
2. After successful login, upgrade to `role: "registered"`
3. Requires email verification (optional for MVP)

### Premium Upgrade Flow
1. User subscribes (email payment, subscription, etc.)
2. Admin updates user role to `premium`
3. User gains access to premium content
4. Session is refreshed with new permissions

## Testing Strategy

### Unit Tests
- Password hashing and verification
- Token generation and validation
- Session creation and expiration
- Role-based access control

### Integration Tests
- Registration flow
- Login flow
- Password reset flow
- Session management

### Security Tests
- Password strength validation
- Rate limiting
- Session hijacking prevention
- Token leakage prevention

## Privacy Considerations

- Store minimal personal data
- Implement data retention policies
- Provide user data export functionality
- Support account deletion with data removal
- GDPR compliance: cookie consent, data subject rights
