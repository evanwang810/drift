"""
Authentication API Endpoints

This module provides authentication-related API endpoints for:
- User registration
- User login
- Password reset
- Profile management
- Session management
"""

import json
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# User database file
USERS_FILE = DATA_DIR / "users.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
TOKENS_FILE = DATA_DIR / "tokens.json"
PASSWORD_RESETS_FILE = DATA_DIR / "password_resets.json"

# Load data from files
def load_users() -> List[Dict]:
    """Load users from JSON file."""
    if not USERS_FILE.exists():
        return []
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users: List[Dict]) -> None:
    """Save users to JSON file."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_sessions() -> List[Dict]:
    """Load sessions from JSON file."""
    if not SESSIONS_FILE.exists():
        return []
    with open(SESSIONS_FILE, 'r') as f:
        return json.load(f)

def save_sessions(sessions: List[Dict]) -> None:
    """Save sessions to JSON file."""
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

def load_tokens() -> List[Dict]:
    """Load tokens from JSON file."""
    if not TOKENS_FILE.exists():
        return []
    with open(TOKENS_FILE, 'r') as f:
        return json.load(f)

def save_tokens(tokens: List[Dict]) -> None:
    """Save tokens to JSON file."""
    with open(TOKENS_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)

def load_password_resets() -> List[Dict]:
    """Load password reset tokens from JSON file."""
    if not PASSWORD_RESETS_FILE.exists():
        return []
    with open(PASSWORD_RESETS_FILE, 'r') as f:
        return json.load(f)

def save_password_resets(resets: List[Dict]) -> None:
    """Save password reset tokens to JSON file."""
    with open(PASSWORD_RESETS_FILE, 'w') as f:
        json.dump(resets, f, indent=2)

def generate_uuid() -> str:
    """Generate a UUID v4."""
    return secrets.token_urlsafe(32)

def generate_session_token() -> str:
    """Generate a secure session token."""
    return secrets.token_urlsafe(64)

def generate_password_reset_token() -> str:
    """Generate a password reset token."""
    return secrets.token_urlsafe(32)

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    Note: This is a placeholder. In production, use bcrypt.
    """
    # Simple hash for demonstration (replace with bcrypt in production)
    import hashlib
    salt = hashlib.sha256(password.encode()).hexdigest()[:16]
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.
    Note: This is a placeholder. In production, use bcrypt.
    """
    # Simple verification for demonstration (replace with bcrypt in production)
    import hashlib
    salt = password_hash[:16]
    expected_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash == expected_hash

def find_user_by_username(users: List[Dict], username: str) -> Optional[Dict]:
    """Find a user by username."""
    for user in users:
        if user.get("username") == username:
            return user
    return None

def find_user_by_email(users: List[Dict], email: str) -> Optional[Dict]:
    """Find a user by email."""
    for user in users:
        if user.get("email") == email:
            return user
    return None

def find_user_by_id(users: List[Dict], user_id: str) -> Optional[Dict]:
    """Find a user by ID."""
    for user in users:
        if user.get("id") == user_id:
            return user
    return None

def find_session_by_token(sessions: List[Dict], token: str) -> Optional[Dict]:
    """Find a session by token."""
    for session in sessions:
        if session.get("token") == token:
            return session
    return None

def find_active_session(sessions: List[Dict], user_id: str) -> Optional[Dict]:
    """Find an active session for a user."""
    now = datetime.now().isoformat()
    for session in sessions:
        if session.get("user_id") == user_id and session.get("expires_at") > now:
            return session
    return None

def clean_expired_sessions() -> None:
    """Remove expired sessions."""
    now = datetime.now().isoformat()
    sessions = load_sessions()
    active_sessions = [s for s in sessions if s.get("expires_at") > now]
    save_sessions(active_sessions)

def clean_expired_tokens() -> None:
    """Remove expired tokens."""
    now = datetime.now().isoformat()
    tokens = load_tokens()
    valid_tokens = [t for t in tokens if t.get("expires_at") > now]
    save_tokens(valid_tokens)

def clean_expired_password_resets() -> None:
    """Remove expired password reset tokens."""
    now = datetime.now().isoformat()
    resets = load_password_resets()
    valid_resets = [r for r in resets if r.get("expires_at") > now]
    save_password_resets(valid_resets)

def get_user_by_session(token: str) -> Optional[Dict]:
    """
    Get user from session token.
    Returns user data or None if invalid/expired session.
    """
    sessions = load_sessions()
    clean_expired_sessions()
    session = find_session_by_token(sessions, token)
    if not session:
        return None

    now = datetime.now().isoformat()
    if session.get("expires_at") <= now:
        return None

    users = load_users()
    user = find_user_by_id(users, session.get("user_id"))
    if user:
        user["last_login"] = datetime.now().isoformat()
        save_users(users)

    return user

def require_auth(token: str) -> Optional[Dict]:
    """
    Require authentication and return user data.
    Returns user data or None if not authenticated.
    """
    user = get_user_by_session(token)
    if not user:
        return None
    return user

# API Endpoints

def handle_register(username: str, email: str, password: str, confirm_password: str) -> Dict:
    """
    Register a new user.
    """
    users = load_users()

    # Check if username already exists
    if find_user_by_username(users, username):
        return {"error": {"message": "Username already exists"}}

    # Check if email already exists
    if find_user_by_email(users, email):
        return {"error": {"message": "Email already registered"}}

    # Check password confirmation
    if password != confirm_password:
        return {"error": {"message": "Passwords do not match"}}

    # Validate password strength (placeholder)
    if len(password) < 12:
        return {"error": {"message": "Password must be at least 12 characters"}}

    # Create new user
    user_id = generate_uuid()
    new_user = {
        "id": user_id,
        "username": username,
        "email": email,
        "password_hash": hash_password(password),
        "role": "registered",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "last_login": None,
        "preferences": {
            "email_notifications": True,
            "newsletter_subscription": True,
            "privacy_consent": True
        },
        "is_active": True,
        "metadata": {}
    }

    users.append(new_user)
    save_users(users)

    return {"success": "Account created successfully"}

def handle_login(username: str, password: str, remember: bool = False) -> Dict:
    """
    User login.
    """
    users = load_users()

    # Find user by username or email
    user = find_user_by_username(users, username)
    if not user:
        user = find_user_by_email(users, username)

    if not user:
        return {"error": {"message": "Invalid username or email"}}

    # Check password
    if not verify_password(password, user.get("password_hash", "")):
        return {"error": {"message": "Invalid password"}}

    # Check if user is active
    if not user.get("is_active", True):
        return {"error": {"message": "Account is inactive"}}

    # Create session
    sessions = load_sessions()
    clean_expired_sessions()

    session_id = generate_uuid()
    session_token = generate_session_token()

    expires_in = 30 * 24 * 3600 if remember else 8 * 3600  # 30 days or 8 hours
    expires_at = (datetime.now() + timedelta(seconds=expires_in)).isoformat()

    new_session = {
        "session_id": session_id,
        "user_id": user["id"],
        "token": session_token,
        "created_at": datetime.now().isoformat(),
        "expires_at": expires_at,
        "ip_address": "127.0.0.1",  # Placeholder
        "user_agent": "Mozilla/5.0",  # Placeholder
        "last_activity": datetime.now().isoformat()
    }

    sessions.append(new_session)
    save_sessions(sessions)

    # Update user last login
    user["last_login"] = datetime.now().isoformat()
    user["updated_at"] = datetime.now().isoformat()
    save_users(users)

    return {
        "success": "Login successful",
        "session_token": session_token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }

def handle_logout(session_token: str) -> Dict:
    """
    User logout.
    """
    sessions = load_sessions()
    session = find_session_by_token(sessions, session_token)

    if session:
        sessions.remove(session)
        save_sessions(sessions)

    return {"success": "Logout successful"}

def handle_reset_password(email: str) -> Dict:
    """
    Request password reset.
    """
    users = load_users()
    user = find_user_by_email(users, email)

    if not user:
        # Don't reveal if user exists for security
        return {"success": "If the email exists, a password reset link will be sent"}

    # Create password reset token
    password_resets = load_password_resets()
    clean_expired_password_resets()

    token = generate_password_reset_token()
    expires_at = (datetime.now() + timedelta(hours=1)).isoformat()

    new_reset = {
        "token": token,
        "user_id": user["id"],
        "created_at": datetime.now().isoformat(),
        "expires_at": expires_at,
        "used": False
    }

    password_resets.append(new_reset)
    save_password_resets(password_resets)

    # In production, send email with reset link
    # This is a placeholder for the email functionality
    reset_link = f"http://localhost:4000/auth/reset-password?token={token}"

    return {
        "success": "Password reset link sent to your email",
        "reset_link": reset_link,
        "expires_in": 3600  # 1 hour
    }

def handle_reset_password_confirm(token: str, new_password: str, confirm_new_password: str) -> Dict:
    """
    Confirm password reset.
    """
    password_resets = load_password_resets()
    clean_expired_password_resets()

    # Find the reset token
    reset_token = None
    for reset in password_resets:
        if reset.get("token") == token and not reset.get("used", False):
            reset_token = reset
            break

    if not reset_token:
        return {"error": {"message": "Invalid or expired reset token"}}

    # Check if token is expired
    if datetime.now().isoformat() > reset_token.get("expires_at"):
        return {"error": {"message": "Reset token has expired"}}

    # Check password confirmation
    if new_password != confirm_new_password:
        return {"error": {"message": "Passwords do not match"}}

    # Validate password strength
    if len(new_password) < 12:
        return {"error": {"message": "Password must be at least 12 characters"}}

    # Update user password
    users = load_users()
    user = find_user_by_id(users, reset_token.get("user_id"))

    if user:
        user["password_hash"] = hash_password(new_password)
        user["updated_at"] = datetime.now().isoformat()
        save_users(users)

    # Mark token as used
    reset_token["used"] = True
    save_password_resets(password_resets)

    return {"success": "Password reset successfully"}

def handle_update_profile(
    session_token: str,
    username: str,
    email: str,
    current_password: str,
    new_password: str
) -> Dict:
    """
    Update user profile.
    """
    # Verify session
    user = get_user_by_session(session_token)
    if not user:
        return {"error": {"message": "Not authenticated"}}

    users = load_users()
    old_user = find_user_by_id(users, user["id"])

    # Verify current password if changing password
    if new_password:
        if not verify_password(current_password, old_user.get("password_hash", "")):
            return {"error": {"message": "Current password is incorrect"}}

        if len(new_password) < 12:
            return {"error": {"message": "New password must be at least 12 characters"}}

        old_user["password_hash"] = hash_password(new_password)
    else:
        # Verify current password if changing other fields
        if not verify_password(current_password, old_user.get("password_hash", "")):
            return {"error": {"message": "Current password is incorrect"}}

    # Check for duplicate username or email
    for u in users:
        if u.get("id") != user["id"]:
            if u.get("username") == username and u.get("email") == email:
                return {"error": {"message": "Username or email already exists"}}

    # Update user
    old_user["username"] = username
    old_user["email"] = email
    old_user["updated_at"] = datetime.now().isoformat()
    save_users(users)

    return {"success": "Profile updated successfully"}
