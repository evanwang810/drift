"""
Flask authentication server for premium content access.
This runs alongside the static site to provide authentication API endpoints.
"""

from flask import Flask, jsonify, request, session, make_response
from functools import wraps
from datetime import datetime, timedelta
import secrets
import os

from site.user_database import UserDatabase
from site.password_manager import PasswordManager

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('AUTH_SECRET_KEY', 'dev-secret-key-change-in-production')

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

    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()

    if username and len(username) >= 3:
        user_db.update_username(session_data['user_id'], username)

    if email and '@' in email:
        user_db.update_email(session_data['user_id'], email)

    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Get current user profile."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({'error': 'Authentication required'}), 401

    session_data = user_db.get_session(session_id)
    if not session_data or not session_data.get('is_valid'):
        return jsonify({'error': 'Invalid session'}), 401

    user = user_db.get_user_by_id(session_data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email']
    }), 200

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Initiate password reset."""
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    user = user_db.get_user_by_email(email)
    if user:
        # Generate reset token
        reset_token = secrets.token_hex(32)
        user_db.create_password_reset_token(user['user_id'], reset_token)
        # In production, send email with reset link
        print(f"Password reset token for {email}: {reset_token}")
        print(f"Reset link: /reset-password?token={reset_token}")

    return jsonify({'message': 'If an account exists with that email, a reset link has been sent'}), 200

@app.route('/api/auth/reset-password/confirm', methods=['POST'])
def confirm_password_reset():
    """Confirm password reset with token."""
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('new_password', '')

    if not token or len(token) < 32 or not new_password or len(new_password) < 8:
        return jsonify({'error': 'Invalid reset token or password'}), 400

    user_id = user_db.verify_password_reset_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    password_manager.update_password(user_id, new_password)
    user_db.delete_password_reset_token(token)

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

    user = user_db.get_user_by_id(session_data['user_id'])
    if not user:
        return jsonify({'authenticated': False}), 200

    return jsonify({
        'authenticated': True,
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email']
    }), 200

if __name__ == '__main__':
    # Create database file if it doesn't exist
    if not user_db.db_path.exists():
        print("Initializing user database...")
        user_db.create_tables()

    print("Starting authentication server on http://localhost:5001")
    print("API endpoints:")
    print("  POST /api/auth/register - Register new user")
    print("  POST /api/auth/login - User login")
    print("  POST /api/auth/logout - User logout")
    print("  GET  /api/auth/status - Check authentication status")
    print("  GET  /api/auth/profile - Get user profile")
    print("  POST /api/auth/profile - Update user profile")
    print("  POST /api/auth/reset-password - Initiate password reset")
    print("  POST /api/auth/reset-password/confirm - Confirm password reset")
    app.run(host='0.0.0.0', port=5001, debug=False)
