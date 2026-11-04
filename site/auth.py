"""Authentication and authorization module for premium content access.

This module provides:
- Password hashing and verification (bcrypt)
- Session management
- User data model and operations
- Role-based access control
- Password reset token management
"""

import json
import secrets
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

import bcrypt


# Paths
ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

USERS_FILE = DOCS / "users.json"
SESSIONS_FILE = DOCS / "sessions.json"
RESET_TOKENS_FILE = DOCS / "reset_tokens.json"

# Constants
SESSION_EXPIRY_HOURS = 24
RESET_TOKEN_EXPIRY_HOURS = 1
PASSWORD_HASH_COST = 12  # Bcrypt cost factor


def load_json_file(filepath: Path) -> Dict[str, Any]:
    """Load JSON file with error handling.

    Args:
        filepath: Path to JSON file

    Returns:
        Dictionary with file contents or empty dict if file doesn't exist
    """
    if not filepath.exists():
        return {"users": [], "sessions": [], "tokens": []}
    try:
        return json.loads(filepath.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        return {"users": [], "sessions": [], "tokens": []}


def save_json_file(filepath: Path, data: Dict[str, Any]) -> None:
    """Save dictionary to JSON file with error handling.

    Args:
        filepath: Path to JSON file
        data: Dictionary to save
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


class User:
    """User data model with authentication support."""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.username = data.get("username")
        self.email = data.get("email")
        self.password_hash = data.get("password_hash")
        self.role = data.get("role", "registered")
        self.created_at = data.get("created_at")
        self.last_login = data.get("last_login")
        self.is_active = data.get("is_active", True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary (without password hash)."""
        result = self.__dict__.copy()
        result.pop("password_hash", None)
        return result


class AuthManager:
    """Authentication and authorization manager."""

    def __init__(self):
        """Initialize auth manager and load data files."""
        self.users_data = load_json_file(USERS_FILE)
        self.sessions_data = load_json_file(SESSIONS_FILE)
        self.reset_tokens_data = load_json_file(RESET_TOKENS_FILE)

    def _save_data(self) -> None:
        """Save all data files."""
        save_json_file(USERS_FILE, self.users_data)
        save_json_file(SESSIONS_FILE, self.sessions_data)
        save_json_file(RESET_TOKENS_FILE, self.reset_tokens_data)

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Bcrypt hash of the password
        """
        salt = bcrypt.gensalt(rounds=PASSWORD_HASH_COST)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against a hash.

        Args:
            password: Plain text password
            password_hash: Bcrypt hash

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except Exception:
            return False

    def create_user(self, username: str, password: str, email: Optional[str] = None) -> Optional[User]:
        """Create a new user account.

        Args:
            username: Desired username (3-50 chars)
            password: Plain text password
            email: User email (optional)

        Returns:
            User object if created, None if username exists
        """
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be 3-50 characters")

        if any(u.get("username") == username for u in self.users_data["users"]):
            return None

        user_id = f"user_{secrets.token_hex(8)}"
        password_hash = self.hash_password(password)

        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "role": "registered",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "last_login": None,
            "is_active": True
        }

        self.users_data["users"].append(user)
        self._save_data()
        return User(user)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve user by username.

        Args:
            username: Username to look up

        Returns:
            User object or None if not found
        """
        for user_data in self.users_data["users"]:
            if user_data.get("username") == username:
                return User(user_data)
        return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve user by ID.

        Args:
            user_id: User ID to look up

        Returns:
            User object or None if not found
        """
        for user_data in self.users_data["users"]:
            if user_data.get("id") == user_id:
                return User(user_data)
        return None

    def create_session(self, user_id: str, user_agent: Optional[str] = None) -> str:
        """Create a new authentication session.

        Args:
            user_id: User ID to create session for
            user_agent: Browser/user agent string (optional)

        Returns:
            Session ID
        """
        session_id = f"sess_{secrets.token_hex(16)}"
        now = datetime.utcnow()

        session = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": now.isoformat() + "Z",
            "expires_at": (now + timedelta(hours=SESSION_EXPIRY_HOURS)).isoformat() + "Z",
            "user_agent": user_agent
        }

        # Clean up expired sessions first
        self._cleanup_expired_sessions()

        self.sessions_data["sessions"].append(session)
        self._save_data()
        return session_id

    def validate_session(self, session_id: str) -> Optional[User]:
        """Validate a session and return the user.

        Args:
            session_id: Session ID to validate

        Returns:
            User object if session is valid, None otherwise
        """
        now = datetime.utcnow()

        # Find the session
        for session_data in self.sessions_data["sessions"]:
            if session_data.get("session_id") == session_id:
                # Check if expired
                if datetime.fromisoformat(session_data["expires_at"]) < now:
                    continue  # Session expired, don't remove yet

                # Get user
                user = self.get_user_by_id(session_data["user_id"])
                if user and user.is_active:
                    # Update last login
                    user.last_login = now.isoformat() + "Z"
                    self._save_user(user.to_dict())
                    return user

        return None

    def destroy_session(self, session_id: str) -> None:
        """Destroy a session.

        Args:
            session_id: Session ID to destroy
        """
        self.sessions_data["sessions"] = [
            s for s in self.sessions_data["sessions"]
            if s.get("session_id") != session_id
        ]
        self._save_data()

    def _cleanup_expired_sessions(self) -> None:
        """Remove all expired sessions from storage."""
        now = datetime.utcnow()
        self.sessions_data["sessions"] = [
            s for s in self.sessions_data["sessions"]
            if datetime.fromisoformat(s["expires_at"]) >= now
        ]

    def _save_user(self, user_data: Dict[str, Any]) -> None:
        """Save user data to users.json.

        Args:
            user_data: User dictionary to save
        """
        for i, user in enumerate(self.users_data["users"]):
            if user.get("id") == user_data["id"]:
                self.users_data["users"][i] = user_data
                break
        self._save_data()

    def create_password_reset_token(self, email: str) -> Optional[str]:
        """Create a password reset token.

        Args:
            email: User email address

        Returns:
            Reset token string, or None if email not found
        """
        user = next((u for u in self.users_data["users"] if u.get("email") == email), None)
        if not user:
            return None

        token = f"reset_{secrets.token_hex(12)}"
        now = datetime.utcnow()

        self.reset_tokens_data["tokens"].append({
            "token": token,
            "user_id": user["id"],
            "email": email,
            "created_at": now.isoformat() + "Z",
            "expires_at": (now + timedelta(hours=RESET_TOKEN_EXPIRY_HOURS)).isoformat() + "Z",
            "used": False
        })

        self._save_data()
        return token

    def validate_password_reset_token(self, token: str) -> Optional[User]:
        """Validate a password reset token.

        Args:
            token: Reset token to validate

        Returns:
            User object if token is valid, None otherwise
        """
        now = datetime.utcnow()

        for token_data in self.reset_tokens_data["tokens"]:
            if token_data.get("token") == token:
                # Check if expired or already used
                if datetime.fromisoformat(token_data["expires_at"]) < now:
                    continue
                if token_data.get("used"):
                    continue

                # Mark as used
                token_data["used"] = True
                self._save_data()

                return self.get_user_by_id(token_data["user_id"])

        return None

    def set_password(self, user_id: str, new_password: str) -> None:
        """Set a new password for a user.

        Args:
            user_id: User ID to update
            new_password: New plain text password
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.password_hash = self.hash_password(new_password)
            self._save_user(user.to_dict())

    def get_role(self, user_id: str) -> str:
        """Get user's role.

        Args:
            user_id: User ID

        Returns:
            Role string (guest, registered, premium)
        """
        user = self.get_user_by_id(user_id)
        if user:
            return user.role
        return "guest"

    def can_access_premium(self, user_id: str) -> bool:
        """Check if user can access premium content.

        Args:
            user_id: User ID

        Returns:
            True if user has premium access, False otherwise
        """
        role = self.get_role(user_id)
        return role == "premium"


# Global auth manager instance
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get or create the global auth manager instance.

    Returns:
        AuthManager instance
    """
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


def init_auth_system() -> None:
    """Initialize the authentication system, creating necessary data files if they don't exist."""
    if not USERS_FILE.exists():
        save_json_file(USERS_FILE, {"users": [], "sessions": [], "tokens": []})
    if not SESSIONS_FILE.exists():
        save_json_file(SESSIONS_FILE, {"users": [], "sessions": [], "tokens": []})
    if not RESET_TOKENS_FILE.exists():
        save_json_file(RESET_TOKENS_FILE, {"users": [], "sessions": [], "tokens": []})


# For testing purposes
if __name__ == "__main__":
    # Test basic authentication
    init_auth_system()
    auth = get_auth_manager()

    print("Testing password hashing...")
    password = "test_password_123"
    hash1 = auth.hash_password(password)
    hash2 = auth.hash_password(password)
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Same hash for same password: {hash1 == hash2}")
    print(f"Verify password works: {auth.verify_password(password, hash1)}")
    print(f"Verify wrong password fails: {not auth.verify_password('wrong_password', hash1)}")

    print("\nTesting user creation...")
    user = auth.create_user("testuser", password, "test@example.com")
    if user:
        print(f"Created user: {user.username} (ID: {user.id})")
    else:
        print("Username already exists")

    print("\nTesting session creation...")
    session_id = auth.create_session(user.id, "Mozilla/5.0")
    print(f"Created session: {session_id}")

    print("\nTesting session validation...")
    validated_user = auth.validate_session(session_id)
    if validated_user:
        print(f"Validated user: {validated_user.username} (role: {validated_user.role})")
    else:
        print("Session invalid")

    print("\nTesting password reset token...")
    token = auth.create_password_reset_token("test@example.com")
    if token:
        print(f"Created reset token: {token}")

    print("\nAll tests completed!")
