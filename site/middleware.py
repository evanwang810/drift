"""
Authentication middleware for protecting premium content routes.
"""

from functools import wraps
from flask import abort, jsonify
from site.auth import has_premium_access


def require_premium(f):
    """
    Decorator that requires premium access to access the route.
    
    Usage:
        @require_premium
        def premium_page():
            return "Premium content"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get session token from request
        session_token = kwargs.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Authentication required', 'code': 'auth_required'}), 401
        
        if not has_premium_access(session_token):
            return jsonify({
                'error': 'Premium content requires paid subscription',
                'code': 'premium_required'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_auth(f):
    """
    Decorator that requires authentication (any role) to access the route.
    
    Usage:
        @require_auth
        def member_page():
            return "Member content"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = kwargs.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Authentication required', 'code': 'auth_required'}), 401
        
        user_data = verify_session(session_token)
        
        if not user_data:
            return jsonify({
                'error': 'Invalid or expired session',
                'code': 'invalid_session'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user(session_token: str):
    """Get current user data from session token."""
    user_data = verify_session(session_token)
    
    if not user_data:
        return None
    
    return {
        'username': user_data['username'],
        'role': user_data['role'],
        'premium_expires': user_data.get('premium_expires')
    }
