"""
Authentication Middleware for Premium Content

This module provides route protection and authentication utilities.
"""

from functools import wraps
from typing import Callable, Optional, Dict
from flask import session, redirect, url_for, flash, g

from user_database import get_user_db


def login_required(f: Callable) -> Callable:
    """
    Decorator to require login for route access.

    Redirects to login page if user is not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session
        user = session.get('user')

        if not user:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))

        # Verify session is valid
        user_db = get_user_db()
        verified_user = user_db.verify_session(user.get('token'))

        if not verified_user:
            session.clear()
            flash('Session expired. Please login again.', 'warning')
            return redirect(url_for('login'))

        # Store verified user in Flask global
        g.user = verified_user
        return f(*args, **kwargs)

    return decorated_function


def premium_required(f: Callable) -> Callable:
    """
    Decorator to require premium role for route access.

    Redirects to login if user is not authenticated or not premium.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session
        user = session.get('user')

        if not user:
            flash('Please login to access premium content', 'warning')
            return redirect(url_for('login'))

        # Verify session is valid
        user_db = get_user_db()
        verified_user = user_db.verify_session(user.get('token'))

        if not verified_user:
            session.clear()
            flash('Session expired. Please login again.', 'warning')
            return redirect(url_for('login'))

        # Check premium access
        if verified_user.get('role') != 'premium':
            flash('Premium content requires a premium subscription', 'info')
            return redirect(url_for('premium_signup'))

        # Store verified user in Flask global
        g.user = verified_user
        return f(*args, **kwargs)

    return decorated_function


def current_user() -> Optional[Dict]:
    """
    Get current authenticated user from session.

    Returns user dict or None if not authenticated.
    """
    user = session.get('user')
    if not user:
        return None

    user_db = get_user_db()
    return user_db.verify_session(user.get('token'))


def logout_user() -> None:
    """Logout current user by revoking session."""
    token = session.get('user', {}).get('token')
    if token:
        user_db = get_user_db()
        user_db.revoke_session(token)
    session.clear()


def create_user_session(user_id: str, token: str) -> None:
    """Create a session for a user."""
    user_db = get_user_db()
    user_db.create_session(user_id, token)
    session['user'] = {
        'id': user_id,
        'token': token
    }


def verify_login(username: str, password: str) -> Optional[Dict]:
    """
    Verify login credentials and return user data if valid.

    Returns user dict or None if invalid.
    """
    user_db = get_user_db()
    success, user = user_db.authenticate_user(username, password)

    if success and user:
        token = secrets.token_urlsafe(32)
        create_user_session(user['id'], token)
        return user

    return None


def require_premium_content(user_id: str) -> bool:
    """
    Check if user has access to premium content.

    Returns True if premium access granted.
    """
    user_db = get_user_db()
    return user_db.check_premium_access(user_id)
