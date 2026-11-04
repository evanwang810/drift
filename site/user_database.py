"""
User Database and Authentication System

This module provides:
- User registration and management
- Session management
- Password hashing and verification
- Role-based access control
"""

import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class UserDatabase:
    """Manages user accounts, sessions, and authentication."""

    def __init__(self, data_dir: str = "site/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.users_file = self.data_dir / "users.json"
        self.sessions_file = self.data_dir / "sessions.json"

        # Load or initialize data
        self.users = self._load_json(self.users_file, {})
        self.sessions = self._load_json(self.sessions_file, {})

    def _load_json(self, file_path: Path, default) -> Dict:
        """Load JSON file or return default dict."""
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return default
        return default

    def _save_json(self, file_path: Path, data: Dict) -> None:
        """Save dict to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def _hash_password(self, password: str) -> str:
        """Hash a password using PBKDF2 with SHA-256."""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hash_obj.hex()}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify a password against stored hash."""
        salt, hash_obj = stored_hash.split('$')
        hash_obj_verify = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hash_obj == hash_obj_verify.hex()

    def register_user(self, username: str, email: str, password: str,
                     role: str = "registered") -> Tuple[bool, str]:
        """
        Register a new user.

        Args:
            username: Desired username (unique)
            email: User's email address
            password: Plain text password
            role: User role (guest, registered, premium)

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate input
        if not username or not email or not password:
            return False, "All fields are required"

        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        # Check if username exists
        if username in self.users:
            return False, "Username already exists"

        # Check if email exists
        for user in self.users.values():
            if user.get('email') == email:
                return False, "Email already registered"

        # Create new user
        user_id = secrets.token_urlsafe(16)
        now = datetime.utcnow().isoformat()

        self.users[user_id] = {
            'id': user_id,
            'username': username,
            'email': email,
            'password_hash': self._hash_password(password),
            'role': role,
            'created_at': now,
            'last_login': None,
            'premium_expires': None
        }

        self._save_json(self.users_file, self.users)
        return True, "Registration successful"

    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Authenticate a user with username and password.

        Args:
            username: Username or email
            password: Plain text password

        Returns:
            Tuple of (success: bool, user_dict: Optional[Dict])
        """
        # Find user by username or email
        user = None
        for uid, u in self.users.items():
            if u.get('username') == username or u.get('email') == username:
                user = u
                break

        if not user:
            return False, None

        # Verify password
        if not self._verify_password(password, user['password_hash']):
            return False, None

        # Update last login
        user['last_login'] = datetime.utcnow().isoformat()
        self._save_json(self.users_file, self.users)

        return True, user

    def create_session(self, user_id: str, token: str) -> None:
        """Create a new session for a user."""
        session = {
            'user_id': user_id,
            'token': token,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(days=7)).isoformat()
        }
        self.sessions[token] = session
        self._save_json(self.sessions_file, self.sessions)

    def verify_session(self, token: str) -> Optional[Dict]:
        """
        Verify a session token and return user data.

        Args:
            token: Session token

        Returns:
            User dict if valid, None otherwise
        """
        if token not in self.sessions:
            return None

        session = self.sessions[token]
        expires_at = datetime.fromisoformat(session['expires_at'])

        if datetime.utcnow() > expires_at:
            # Session expired, delete it
            del self.sessions[token]
            self._save_json(self.sessions_file, self.sessions)
            return None

        # Return user data (exclude password hash)
        user = self.users.get(session['user_id'])
        if not user:
            return None

        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'last_login': user['last_login']
        }

    def revoke_session(self, token: str) -> None:
        """Revoke a session."""
        if token in self.sessions:
            del self.sessions[token]
            self._save_json(self.sessions_file, self.sessions)

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID."""
        user = self.users.get(user_id)
        if user:
            # Exclude password hash
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at'],
                'last_login': user['last_login'],
                'premium_expires': user.get('premium_expires')
            }
        return None

    def update_user_role(self, user_id: str, role: str) -> bool:
        """Update a user's role."""
        if user_id not in self.users:
            return False

        self.users[user_id]['role'] = role
        self._save_json(self.users_file, self.users)
        return True

    def check_premium_access(self, user_id: str) -> bool:
        """
        Check if user has premium access.

        Returns True if user has premium role or premium subscription active.
        """
        user = self.users.get(user_id)
        if not user:
            return False

        # Check role
        if user.get('role') == 'premium':
            return True

        # Check premium expiration
        premium_expires = user.get('premium_expires')
        if premium_expires:
            expires_at = datetime.fromisoformat(premium_expires)
            return datetime.utcnow() <= expires_at

        return False

    def list_users(self, limit: int = 100) -> List[Dict]:
        """List all users (for admin purposes)."""
        users = []
        for uid, user in self.users.items():
            users.append({
                'id': uid,
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at'],
                'last_login': user.get('last_login')
            })
        return users[:limit]

    def delete_user(self, user_id: str) -> bool:
        """Delete a user account."""
        if user_id not in self.users:
            return False

        # Also delete associated sessions
        sessions_to_delete = [token for token, session in self.sessions.items()
                             if session.get('user_id') == user_id]
        for token in sessions_to_delete:
            del self.sessions[token]

        del self.users[user_id]
        self._save_json(self.users_file, self.users)
        self._save_json(self.sessions_file, self.sessions)
        return True


# Global instance
_user_db = None


def get_user_db() -> UserDatabase:
    """Get or create the global user database instance."""
    global _user_db
    if _user_db is None:
        _user_db = UserDatabase()
    return _user_db
