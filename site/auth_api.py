"""
Authentication API endpoints for user registration, login, and password management.
"""

import os
import secrets
import string
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from user_database import UserManager
from password_manager import PasswordManager

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Initialize managers
user_manager = UserManager()
password_manager = PasswordManager()

# Session config
SESSION_TIMEOUT = timedelta(hours=24)
TOKEN_EXPIRY = timedelta(hours=1)


@auth_bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'GET':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        # Validate input
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400

        if len(username) < 3 or len(username) > 30:
            return jsonify({'error': 'Username must be between 3 and 30 characters'}), 400

        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400

        # Check if user exists
        if user_manager.user_exists(username):
            return jsonify({'error': 'Username already exists'}), 409

        if user_manager.email_exists(email):
            return jsonify({'error': 'Email already registered'}), 409

        # Hash password and create user
        password_hash = password_manager.hash_password(password)
        user_id = user_manager.create_user(username, email, password_hash)

        # Set up session
        session['user_id'] = user_id
        session['username'] = username
        session['premium'] = False
        session['created_at'] = datetime.utcnow().isoformat()
        session['token'] = secrets.token_urlsafe(32)

        return jsonify({
            'message': 'Registration successful',
            'user_id': user_id,
            'username': username,
            'premium': False
        }), 201


@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('auth.profile'))
        return 'login', 200  # Render template

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        # Validate input
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Get user
        user = user_manager.get_user(username)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Verify password
        if not password_manager.verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Check if account is active
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is inactive'}), 403

        # Set up session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['email'] = user['email']
        session['premium'] = user.get('premium', False)
        session['created_at'] = user.get('created_at', datetime.utcnow().isoformat())
        session['token'] = secrets.token_urlsafe(32)

        return jsonify({
            'message': 'Login successful',
            'user_id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'premium': user.get('premium', False)
        }), 200


@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Handle user logout."""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/auth/profile', methods=['GET'])
def profile():
    """Get current user profile."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    user_id = session['user_id']
    user = user_manager.get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user_id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'premium': user.get('premium', False),
        'created_at': user.get('created_at'),
        'is_active': user.get('is_active', True)
    }), 200


@auth_bp.route('/auth/change-password', methods=['POST'])
def change_password():
    """Handle password change."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    # Validate input
    if not current_password or not new_password or not confirm_password:
        return jsonify({'error': 'All password fields are required'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'New passwords do not match'}), 400

    if len(new_password) < 8:
        return jsonify({'error': 'New password must be at least 8 characters'}), 400

    # Get user
    user_id = session['user_id']
    user = user_manager.get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Verify current password
    if not password_manager.verify_password(current_password, user['password_hash']):
        return jsonify({'error': 'Current password is incorrect'}), 401

    # Update password
    new_password_hash = password_manager.hash_password(new_password)
    user_manager.update_password(user_id, new_password_hash)

    return jsonify({'message': 'Password changed successfully'}), 200


@auth_bp.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """Send password reset email."""
    data = request.get_json()
    email = data.get('email', '').strip()

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Get user by email
    user = user_manager.get_user_by_email(email)

    if not user:
        # Don't reveal if email exists for security
        return jsonify({'message': 'If an account exists with this email, a reset link will be sent'}), 200

    # Generate reset token
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + TOKEN_EXPIRY

    # Store reset token
    user_manager.store_reset_token(user['id'], token, expiry)

    # In production, send actual email here
    # For now, return the reset URL (this would normally be an email)
    reset_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:5000')}/auth/reset-password-confirm?token={token}"

    return jsonify({
        'message': 'Password reset link sent',
        'reset_url': reset_url
    }), 200


@auth_bp.route('/auth/reset-password-confirm', methods=['GET'])
def reset_password_confirm():
    """Display password reset confirmation page."""
    token = request.args.get('token', '')

    if not token:
        return 'Invalid or missing token', 400

    return 'reset_password_confirm', 200  # Render template


@auth_bp.route('/auth/reset-password-confirm', methods=['POST'])
def reset_password_confirm_post():
    """Handle password reset confirmation."""
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    # Validate input
    if not token or not new_password or not confirm_password:
        return jsonify({'error': 'All fields are required'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if len(new_password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    # Verify token
    user = user_manager.verify_reset_token(token)

    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400

    # Update password
    new_password_hash = password_manager.hash_password(new_password)
    user_manager.update_password(user['id'], new_password_hash)
    user_manager.clear_reset_token(user['id'])

    return jsonify({'message': 'Password reset successfully'}), 200


@auth_bp.route('/auth/verify-token', methods=['GET'])
def verify_token():
    """Verify authentication token."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    user_id = session['user_id']
    user = user_manager.get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'authenticated': True,
        'user_id': user['id'],
        'username': user['username'],
        'premium': user.get('premium', False)
    }), 200


@auth_bp.route('/auth/premium', methods=['GET'])
def check_premium():
    """Check if user has premium access."""
    if 'user_id' not in session:
        return jsonify({'premium': False}), 200

    user_id = session['user_id']
    user = user_manager.get_user_by_id(user_id)

    if not user:
        return jsonify({'premium': False}), 200

    return jsonify({'premium': user.get('premium', False)}), 200
