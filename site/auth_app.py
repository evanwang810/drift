"""
Authentication API endpoints for premium content access.
"""

from flask import Flask, request, jsonify, session
from functools import wraps
import secrets
from datetime import datetime, timedelta
import os

from user_database import UserDatabase
from password_manager import PasswordManager

app = Flask(__name__)
app.secret_key = os.environ.get('AUTH_SECRET_KEY', secrets.token_hex(32))

# Initialize database and password manager
user_db = UserDatabase()
password_manager = PasswordManager()

# Premium content protected routes decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return jsonify({'error': 'Authentication required'}), 401

        session_data = user_db.get_session(session_id)
        if not session_data or not session_data.get('is_valid'):
            return jsonify({'error': 'Invalid or expired session'}), 401

        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user account."""
    data = request.get_json()

    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    # Validation
    if not username or len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400

    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    if not password or len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    # Check if user already exists
    if user_db.user_exists(username):
        return jsonify({'error': 'Username already taken'}), 409

    if user_db.email_exists(email):
        return jsonify({'error': 'Email already registered'}), 409

    # Create user
    user_id = user_db.create_user(username, email, password)
    if not user_id:
        return jsonify({'error': 'Failed to create user'}), 500

    return jsonify({'message': 'Registration successful', 'user_id': user_id}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint."""
    data = request.get_json()

    username = data.get('username', '').strip()
    password = data.get('password', '')

    # Get user
    user = user_db.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Verify password
    if not password_manager.verify_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create session
    session_id = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    user_db.create_session(session_id, user['user_id'], expires_at)

    # Set secure cookie
    response = jsonify({
        'message': 'Login successful',
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email']
    })
    response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Strict')

    return response, 200

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint."""
    session_id = request.cookies.get('session_id')

    if session_id:
        user_db.delete_session(session_id)

    response = jsonify({'message': 'Logout successful'})
    response.set_cookie('session_id', '', expires=0)
    return response, 200

@app.route('/api/auth/profile', methods=['POST'])
def update_profile():
    """Update user profile."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({'error': 'Authentication required'}), 401

    session_data = user_db.get_session(session_id)
    if not session_data or not session_data.get('is_valid'):
        return jsonify({'error': 'Invalid session'}), 401

    user_id = session_data['user_id']
    data = request.get_json()

    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_new_password = data.get('confirm_new_password', '')

    # Validation
    if not username or len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400

    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    # Get current user
    user = user_db.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check current password if trying to change password
    if new_password:
        if not current_password:
            return jsonify({'error': 'Current password required to change password'}), 400

        if not password_manager.verify_password(current_password, user['password_hash']):
            return jsonify({'error': 'Current password is incorrect'}), 401

        if new_password != confirm_new_password:
            return jsonify({'error': 'New passwords do not match'}), 400

        if len(new_password) < 8:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400

        # Update password
        user_db.update_password(user_id, new_password)

    # Update profile info
    if username != user['username']:
        if user_db.user_exists(username):
            return jsonify({'error': 'Username already taken'}), 409
        user_db.update_username(user_id, username)

    if email != user['email']:
        if user_db.email_exists(email):
            return jsonify({'error': 'Email already registered'}), 409
        user_db.update_email(user_id, email)

    # Refresh session
    user_db.delete_session(session_id)
    session_id = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    user_db.create_session(session_id, user_id, expires_at)

    response = jsonify({
        'message': 'Profile updated successfully',
        'user_id': user_id,
        'username': username,
        'email': email
    })
    response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Strict')

    return response, 200

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Request password reset."""
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    user = user_db.get_user_by_email(email)
    if user:
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        user_db.create_password_reset(user['user_id'], reset_token, expires_at)

        # TODO: Send email with reset link
        # For now, we'll log it for testing
        print(f"Password reset token for {email}: {reset_token}")

    return jsonify({'message': 'If an account exists with this email, a reset link has been sent'}), 200

@app.route('/api/auth/reset-password/confirm', methods=['POST'])
def confirm_password_reset():
    """Confirm password reset with token."""
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    if not token:
        return jsonify({'error': 'Reset token required'}), 400

    if not new_password or len(new_password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Validate and use token
    user_id = user_db.validate_password_reset_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    # Update password
    user_db.update_password(user_id, new_password)

    # Delete used token
    user_db.delete_password_reset(token)

    return jsonify({'message': 'Password reset successfully'}), 200

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status."""
    session_id = request.cookies.get('session_id')

    if not session_id:
        return jsonify({'authenticated': False}), 200

    session_data = user_db.get_session(session_id)
    if not session_data or not session_data.get('is_valid'):
        return jsonify({'authenticated': False}), 200

    user = user_db.get_user(session_data['user_id'])
    if not user:
        return jsonify({'authenticated': False}), 200

    return jsonify({
        'authenticated': True,
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email']
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
