"""API endpoints for user authentication.

This module provides endpoints for:
- User registration
- User login
- Password reset (request and reset)
- User logout
- Get user profile
"""

from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from agent.tools import user_database

auth_bp = Blueprint('auth', __name__)

# Session cookie settings
SESSION_DURATION = timedelta(days=7)


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user.
    
    Expected JSON:
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    
    Returns:
        {
            "success": true,
            "message": "User registered successfully",
            "user": {...}
        }
    """
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: username, email, password"
        }), 400
    
    username = data['username'].strip()
    email = data['email'].strip()
    password = data['password']
    
    # Validate inputs
    if len(username) < 3:
        return jsonify({
            "success": False,
            "message": "Username must be at least 3 characters"
        }), 400
    
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters"
        }), 400
    
    # Check if user already exists
    existing_user = user_database.get_user_by_username(username)
    if existing_user:
        return jsonify({
            "success": False,
            "message": "Username already exists"
        }), 409
    
    existing_email = user_database.get_user_by_email(email)
    if existing_email:
        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 409
    
    # Create new user
    user_id = user_database.create_user(username, email, password)
    
    if not user_id:
        return jsonify({
            "success": False,
            "message": "Failed to create user"
        }), 500
    
    user = user_database.get_user_by_id(user_id)
    
    # Log in the user automatically
    session['user_id'] = user_id
    session['username'] = user['username']
    session['email'] = user['email']
    session['is_premium'] = user['is_premium']
    session['is_admin'] = user['is_admin']
    session['last_login'] = datetime.utcnow().isoformat()
    
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user": {
            "id": user_id,
            "username": user['username'],
            "email": user['email'],
            "is_premium": user['is_premium'],
            "is_admin": user['is_admin'],
            "created_at": user['created_at']
        }
    }), 201


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Log in a user.
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns:
        {
            "success": true,
            "message": "Login successful",
            "user": {...}
        }
    """
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: username, password"
        }), 400
    
    username = data['username'].strip()
    password = data['password']
    
    # Get user
    user = user_database.get_user_by_username(username)
    
    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401
    
    # Verify password
    if not user_database.verify_password(user['id'], password):
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401
    
    # Update last login
    user_database.update_last_login(user['id'])
    
    # Set session
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['email'] = user['email']
    session['is_premium'] = user['is_premium']
    session['is_admin'] = user['is_admin']
    session['last_login'] = datetime.utcnow().isoformat()
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "is_premium": user['is_premium'],
            "is_admin": user['is_admin'],
            "last_login": user['last_login']
        }
    }), 200


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Log out the current user.
    
    Returns:
        {
            "success": true,
            "message": "Logged out successfully"
        }
    """
    session.clear()
    
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200


@auth_bp.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Get the currently authenticated user's profile.
    
    Requires authentication.
    
    Returns:
        {
            "success": true,
            "user": {...}
        }
    """
    if 'user_id' not in session:
        return jsonify({
            "success": False,
            "message": "Not authenticated"
        }), 401
    
    user = user_database.get_user_by_id(session['user_id'])
    
    if not user:
        session.clear()
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    
    return jsonify({
        "success": True,
        "user": {
            "id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "is_premium": user['is_premium'],
            "is_admin": user['is_admin'],
            "created_at": user['created_at'],
            "last_login": user['last_login']
        }
    }), 200


@auth_bp.route('/api/auth/password-reset-request', methods=['POST'])
def password_reset_request():
    """Request a password reset email.
    
    Expected JSON:
    {
        "email": "string"
    }
    
    Returns:
        {
            "success": true,
            "message": "If email exists, reset link sent"
        }
    """
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({
            "success": False,
            "message": "Missing email field"
        }), 400
    
    email = data['email'].strip()
    
    user = user_database.get_user_by_email(email)
    
    if not user:
        # Don't reveal if email exists or not for security
        return jsonify({
            "success": True,
            "message": "If this email is registered, a password reset link will be sent"
        }), 200
    
    # Generate reset token
    reset_token = user_database.create_password_reset_token(user['id'])
    
    # In production, send email here. For now, return the token
    # TODO: Implement email sending
    return jsonify({
        "success": True,
        "message": "Password reset link sent (development mode: token provided below)",
        "reset_token": reset_token,
        "user_id": user['id']
    }), 200


@auth_bp.route('/api/auth/password-reset', methods=['POST'])
def password_reset():
    """Reset a password using a reset token.
    
    Expected JSON:
    {
        "token": "string",
        "new_password": "string"
    }
    
    Returns:
        {
            "success": true,
            "message": "Password reset successfully"
        }
    """
    data = request.get_json()
    
    if not data or 'token' not in data or 'new_password' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: token, new_password"
        }), 400
    
    token = data['token']
    new_password = data['new_password']
    
    # Validate password
    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters"
        }), 400
    
    # Reset password
    success = user_database.reset_password(token, new_password)
    
    if not success:
        return jsonify({
            "success": False,
            "message": "Invalid or expired reset token"
        }), 400
    
    return jsonify({
        "success": True,
        "message": "Password reset successfully"
    }), 200


@auth_bp.route('/api/auth/verify', methods=['POST'])
def verify_session():
    """Verify the current session is still valid.
    
    Returns:
        {
            "success": true,
            "valid": true/false
        }
    """
    if 'user_id' not in session:
        return jsonify({
            "success": True,
            "valid": False
        }), 200
    
    user = user_database.get_user_by_id(session['user_id'])
    
    if not user:
        session.clear()
        return jsonify({
            "success": True,
            "valid": False
        }), 200
    
    return jsonify({
        "success": True,
        "valid": True
    }), 200
