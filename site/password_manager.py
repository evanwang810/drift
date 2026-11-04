"""
Password Management and Verification System

Provides secure password hashing, verification, and strength checking.
"""

import bcrypt
import re
from typing import Tuple


class PasswordManager:
    """Manages password security operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Bcrypt hash of the password
        """
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            password: Plain text password
            password_hash: Stored password hash

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False

    @staticmethod
    def check_password_strength(password: str) -> Tuple[bool, str]:
        """
        Check password strength and return validation status.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, message)
        """
        # Minimum length check
        if len(password) < 12:
            return False, "Password must be at least 12 characters long"

        # Length check
        if len(password) > 128:
            return False, "Password must be at most 128 characters long"

        # Check for mixed case
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        # Check for lowercase
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        # Check for numbers
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"

        # Check for special characters
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"

        # Check for common patterns (basic)
        if re.search(r'(password|123456|qwerty|admin)', password.lower()):
            return False, "Password is too common or weak"

        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            return False, "Password contains repeated characters"

        return True, "Password meets all requirements"

    @staticmethod
    def generate_password(length: int = 16) -> str:
        """
        Generate a random secure password.

        Args:
            length: Password length (default: 16)

        Returns:
            Generated password
        """
        import secrets
        import string

        if length < 12:
            length = 12
        if length > 32:
            length = 32

        # Define character sets
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special = string.punctuation

        # Ensure at least one of each character type
        password = [
            secrets.choice(uppercase),
            secrets.choice(lowercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]

        # Fill the rest with random characters
        all_chars = uppercase + lowercase + digits + special
        for _ in range(length - 4):
            password.append(secrets.choice(all_chars))

        # Shuffle the password
        import random
        random.shuffle(password)

        return ''.join(password)
