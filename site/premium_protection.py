"""
Premium content protection middleware.
"""

from flask import Flask, abort, jsonify
from functools import wraps
import os
from datetime import datetime

from site.user_database import UserDatabase
from site.password_manager import PasswordManager

# Initialize database and password manager
user_db = UserDatabase()
password_manager = PasswordManager()

def is_premium_route(path):
    """Check if a route requires premium access."""
    premium_paths = [
        '/premium',
        '/premium/.*',
    ]
    return any(__import__('re').match(pattern, path) for pattern in premium_paths)

def require_premium(f):
    """
    Decorator to protect routes requiring premium access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if route requires premium
        request_path = request.path
        if not is_premium_route(request_path):
            return f(*args, **kwargs)

        # Get session ID from cookie
        session_id = request.cookies.get('session_id')

        if not session_id:
            return jsonify({
                'error': 'Premium content requires authentication',
                'premium_required': True
            }), 401

        # Validate session
        session_data = user_db.get_session(session_id)
        if not session_data:
            return jsonify({
                'error': 'Invalid or expired session',
                'premium_required': True
            }), 401

        if not session_data.get('is_valid'):
            return jsonify({
                'error': 'Session expired',
                'premium_required': True
            }), 401

        # Check user subscription status
        user_id = session_data['user_id']
        user = user_db.get_user(user_id)

        if not user or user.get('subscription_status') != 'premium':
            return jsonify({
                'error': 'Premium content requires a premium subscription',
                'premium_required': True
            }), 403

        # Check if subscription is active
        if user.get('subscription_expires_at'):
            expires_at = datetime.fromisoformat(user['subscription_expires_at'])
            if expires_at < datetime.utcnow():
                return jsonify({
                    'error': 'Premium subscription has expired',
                    'premium_required': True
                }), 403

        return f(*args, **kwargs)

    return decorated_function

def ensure_premium_template(f):
    """
    Decorator to protect Jinja2 templates requiring premium access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get template path
        template_name = kwargs.get('template_name')

        if not template_name:
            return f(*args, **kwargs)

        # Check if template requires premium
        if template_name.startswith('premium/') or '/premium/' in template_name:
            # Get session ID from request context
            session_id = getattr(request, 'session_id', None)

            if not session_id:
                # Try to get from cookie
                session_id = request.cookies.get('session_id')

            if not session_id:
                return jsonify({
                    'error': 'Premium content requires authentication',
                    'premium_required': True
                }), 401

            # Validate session
            session_data = user_db.get_session(session_id)
            if not session_data:
                return jsonify({
                    'error': 'Invalid or expired session',
                    'premium_required': True
                }), 401

            if not session_data.get('is_valid'):
                return jsonify({
                    'error': 'Session expired',
                    'premium_required': True
                }), 401

            # Check user subscription status
            user_id = session_data['user_id']
            user = user_db.get_user(user_id)

            if not user or user.get('subscription_status') != 'premium':
                return jsonify({
                    'error': 'Premium content requires a premium subscription',
                    'premium_required': True
                }), 403

            # Check if subscription is active
            if user.get('subscription_expires_at'):
                expires_at = datetime.fromisoformat(user['subscription_expires_at'])
                if expires_at < datetime.utcnow():
                    return jsonify({
                        'error': 'Premium subscription has expired',
                        'premium_required': True
                    }), 403

        return f(*args, **kwargs)

    return decorated_function
