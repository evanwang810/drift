"""
Premium content protection middleware.
"""

from flask import Flask, abort, jsonify, session as flask_session
from functools import wraps
from datetime import datetime

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

        # Check if user is authenticated via Flask session
        if 'user_id' not in flask_session:
            return jsonify({
                'error': 'Premium content requires authentication',
                'premium_required': True
            }), 401

        # Get user from database
        from site.user_database import UserDatabase
        user_db = UserDatabase()
        user_id = flask_session['user_id']
        user = user_db.get_user(user_id)

        if not user:
            return jsonify({
                'error': 'User not found',
                'premium_required': True
            }), 404

        # Check user subscription status
        if user.get('subscription_status') != 'premium':
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
            # Check if user is authenticated via Flask session
            if 'user_id' not in flask_session:
                return jsonify({
                    'error': 'Premium content requires authentication',
                    'premium_required': True
                }), 401

            # Get user from database
            from site.user_database import UserDatabase
            user_db = UserDatabase()
            user_id = flask_session['user_id']
            user = user_db.get_user(user_id)

            if not user:
                return jsonify({
                    'error': 'User not found',
                    'premium_required': True
                }), 404

            # Check user subscription status
            if user.get('subscription_status') != 'premium':
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
