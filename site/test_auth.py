#!/usr/bin/env python3
"""
Test script for authentication system.
Creates test users and verifies all authentication flows work correctly.
"""

import sys
import os

# Add site to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site'))

from user_database import UserDatabase
from password_manager import PasswordManager
import secrets
from datetime import datetime, timedelta

def test_authentication():
    """Test all authentication flows."""
    print("=" * 60)
    print("Authentication System Test")
    print("=" * 60)

    # Initialize components
    user_db = UserDatabase()
    password_manager = PasswordManager()

    # Test 1: Create users
    print("\n1. Testing user creation...")
    success, success, user1_id = user_db.register_user("testuser1", "test1@example.com", "TestPassword123!")
    success, success2, user2_id = user_db.register_user("testuser2", "test2@example.com", "TestPassword123!")

    if user1_id and user2_id:
        print("✓ Users created successfully")
    else:
        print("✗ Failed to create users")
        return False

    # Test 2: Password hashing and verification
    print("\n2. Testing password hashing and verification...")
    test_password = "TestPassword123!"
    user1 = user_db.get_user(user1_id) if user1_id else None

    if password_manager.verify_password(test_password, user1['password_hash']):
        print("✓ Password verification works")
    else:
        print("✗ Password verification failed")
        return False

    # Test 3: User registration
    print("\n3. Testing user registration...")
    if user_db.user_exists("testuser1") and user_db.email_exists("test1@example.com"):
        print("✓ User registration works")
    else:
        print("✗ User registration failed")
        return False

    # Test 4: Login and session creation
    print("\n4. Testing login and session creation...")
    session_id = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    session_created = user_db.create_session(session_id, user1_id, expires_at)

    if session_created:
        print("✓ Session created successfully")
    else:
        print("✗ Failed to create session")
        return False

    # Test 5: Session validation
    print("\n5. Testing session validation...")
    session_data = user_db.get_session(session_id)
    if session_data and session_data.get('is_valid'):
        print("✓ Session validation works")
    else:
        print("✗ Session validation failed")
        return False

    # Test 6: Get user by session
    print("\n6. Testing user retrieval by session...")
    user_from_session = user_db.get_user(session_data['user_id'])
    if user_from_session and user_from_session['username'] == "testuser1":
        print("✓ User retrieval by session works")
    else:
        print("✗ User retrieval by session failed")
        return False

    # Test 7: Session expiration
    print("\n7. Testing session expiration...")
    expired_session_id = secrets.token_hex(32)
    expired_session_created = user_db.create_session(
        expired_session_id,
        user1_id,
        datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago
    )

    if expired_session_created:
        expired_session_data = user_db.get_session(expired_session_id)
        if not expired_session_data or not expired_session_data.get('is_valid'):
            print("✓ Session expiration works")
        else:
            print("✗ Session expiration failed")
            return False

    # Test 8: Logout and session deletion
    print("\n8. Testing logout and session deletion...")
    user_db.delete_session(session_id)
    session_after_logout = user_db.get_session(session_id)
    if not session_after_logout:
        print("✓ Logout works")
    else:
        print("✗ Logout failed")
        return False

    # Test 9: Password reset flow
    print("\n9. Testing password reset flow...")
    reset_token = secrets.token_urlsafe(32)
    reset_created = user_db.create_password_reset(user1_id, reset_token, datetime.utcnow() + timedelta(hours=1))

    if reset_created:
        print("✓ Password reset token created")

        # Validate token
        token_user_id = user_db.validate_password_reset_token(reset_token)
        if token_user_id == user1_id:
            print("✓ Password reset token validation works")

            # Update password
            new_password = "NewPassword456!"
            user_db.update_password(user1_id, new_password)

            # Verify new password
            user = user_db.get_user(user1_id)
            if password_manager.verify_password(new_password, user['password_hash']):
                print("✓ Password update works")
            else:
                print("✗ Password update failed")
                return False
        else:
            print("✗ Password reset token validation failed")
            return False
    else:
        print("✗ Failed to create password reset token")
        return False

    # Test 10: User profile updates
    print("\n10. Testing user profile updates...")
    user_db.update_username(user1_id, "updateduser")
    user_db.update_email(user1_id, "updated1@example.com")

    updated_user = user_db.get_user(user1_id)
    if (updated_user['username'] == "updateduser" and
        updated_user['email'] == "updated1@example.com"):
        print("✓ User profile updates work")
    else:
        print("✗ User profile updates failed")
        return False

    # Test 11: Password change
    print("\n11. Testing password change...")
    current_password = "NewPassword456!"
    new_password = "FinalPassword789!"
    user_db.update_password(user1_id, new_password)

    user = user_db.get_user(user1_id)
    if password_manager.verify_password(new_password, user['password_hash']):
        print("✓ Password change works")
    else:
        print("✗ Password change failed")
        return False

    print("\n" + "=" * 60)
    print("All authentication tests passed! ✓")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_authentication()
    sys.exit(0 if success else 1)
