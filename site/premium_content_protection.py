"""
Premium Content Protection Middleware

This module provides decorators and utilities for protecting premium content
with proper authentication and authorization checks.
"""

from functools import wraps
from typing import Callable, Optional
from flask import redirect, url_for, flash, session

from auth_middleware import current_user, logout_user


def premium_required(f: Callable) -> Callable:
    """
    Decorator to require premium role for route access.

    Redirects to login if user is not authenticated or not premium.

    Usage:
        @app.route('/premium-docs')
        @premium_required
        def premium_docs():
            return render_template('premium-docs.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user()

        if not user:
            flash('Please login to access premium content', 'warning')
            return redirect(url_for('login'))

        if user.get('role') != 'premium':
            flash('Premium content requires a Premium subscription', 'info')
            return redirect(url_for('premium_signup'))

        return f(*args, **kwargs)

    return decorated_function


def auth_or_premium_required(f: Callable) -> Callable:
    """
    Decorator to require authentication OR premium role.

    Allows guests to view basic content, but requires login for premium
    content, and premium role for premium-only content.

    Usage:
        @app.route('/content')
        @auth_or_premium_required
        def content():
            user = current_user()
            if user and user.get('role') == 'premium':
                return render_template('premium-content.html')
            return render_template('basic-content.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user()

        if not user:
            flash('Please login to access this content', 'warning')
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function


def check_premium_access() -> bool:
    """
    Check if current user has premium access.

    Returns True if user is authenticated and has premium role.
    """
    user = current_user()
    return user is not None and user.get('role') == 'premium'


def get_premium_status() -> dict:
    """
    Get premium access status for current user.

    Returns dict with status information.
    """
    user = current_user()

    if not user:
        return {
            'authenticated': False,
            'premium': False,
            'message': 'Please login to access premium features'
        }

    return {
        'authenticated': True,
        'premium': user.get('role') == 'premium',
        'role': user.get('role'),
        'message': 'You have Premium access' if user.get('role') == 'premium' else 'You have Registered access'
    }


def get_user_info() -> Optional[dict]:
    """
    Get information about current authenticated user.

    Returns user dict or None if not authenticated.
    """
    return current_user()
