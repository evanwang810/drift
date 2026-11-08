#!/usr/bin/env python3
"""
Authentication API for the repository website.
Handles user registration, login, logout, password reset, and profile management.
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus

# Flask imports (must be at top level for module import)
from flask import Flask, request, jsonify

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'user_database.db')

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the user database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'registered',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')

    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Password reset tokens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def require_auth(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from header or cookie
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return jsonify({'error': 'Authentication required'}), HTTPStatus.UNAUTHORIZED

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if token is valid
        cursor.execute('''
            SELECT s.user_id, u.username, u.email, u.role
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ? AND s.expires_at > ?
        ''', (token, datetime.utcnow()))

        session = cursor.fetchone()
        conn.close()

        if not session:
            return jsonify({'error': 'Invalid or expired token'}), HTTPStatus.UNAUTHORIZED

        # Add user to request
        request.user = dict(session)

        return f(*args, **kwargs)

    return decorated_function

def verify_password(password_hash, password):
    """Verify a password against a hash."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest() == password_hash

def hash_password(password):
    """Hash a password using SHA-256."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    """Generate a random session token."""
    import secrets
    return secrets.token_urlsafe(32)

def generate_reset_token():
    """Generate a random password reset token."""
    import secrets
    return secrets.token_urlsafe(32)

# Initialize database on import
init_db()

# API Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        # Validate input
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), HTTPStatus.BAD_REQUEST

        if len(username) < 3 or len(username) > 50:
            return jsonify({'error': 'Username must be 3-50 characters'}), HTTPStatus.BAD_REQUEST

        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Username or email already exists'}), HTTPStatus.CONFLICT

        # Create new user
        password_hash = hash_password(password)
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'username': username
        }), HTTPStatus.CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login a user."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get user
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if not user or not verify_password(user['password_hash'], password):
            conn.close()
            return jsonify({'error': 'Invalid username or password'}), HTTPStatus.UNAUTHORIZED

        # Check if user is banned or inactive
        if user['role'] == 'banned':
            conn.close()
            return jsonify({'error': 'Account has been banned'}), HTTPStatus.FORBIDDEN

        # Create session
        token = generate_token()
        expires_at = datetime.utcnow() + timedelta(days=7)

        cursor.execute(
            'INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)',
            (user['id'], token, expires_at)
        )

        # Update last login
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', (datetime.utcnow(), user['id']))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout a user."""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return jsonify({'error': 'Token required'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete session
        cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Logout successful'}), HTTPStatus.OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/auth/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get current user profile."""
    try:
        return jsonify({
            'username': request.user['username'],
            'email': request.user['email'],
            'role': request.user['role']
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/auth/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update current user profile."""
    try:
        data = request.get_json()
        username = data.get('username', request.user['username']).strip()
        email = data.get('email', request.user['email']).strip().lower()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        confirm_new_password = data.get('confirm_new_password', '')

        # Validate username
        if len(username) < 3 or len(username) > 50:
            return jsonify({'error': 'Username must be 3-50 characters'}), HTTPStatus.BAD_REQUEST

        # Validate email
        if not email:
            return jsonify({'error': 'Email is required'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username is taken by another user
        cursor.execute('SELECT id FROM users WHERE username = ? AND id != ?', (username, request.user['id']))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Username already taken'}), HTTPStatus.CONFLICT

        # Check if email is taken by another user
        cursor.execute('SELECT id FROM users WHERE email = ? AND id != ?', (email, request.user['id']))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Email already taken'}), HTTPStatus.CONFLICT

        # Update username and email
        cursor.execute(
            'UPDATE users SET username = ?, email = ? WHERE id = ?',
            (username, email, request.user['id'])
        )

        # Update password if provided
        if new_password:
            if len(new_password) < 8:
                conn.close()
                return jsonify({'error': 'New password must be at least 8 characters'}), HTTPStatus.BAD_REQUEST

            if new_password != confirm_new_password:
                conn.close()
                return jsonify({'error': 'New passwords do not match'}), HTTPStatus.BAD_REQUEST

            if not current_password:
                conn.close()
                return jsonify({'error': 'Current password is required to change password'}), HTTPStatus.BAD_REQUEST

            # Verify current password
            cursor.execute('SELECT password_hash FROM users WHERE id = ?', (request.user['id'],))
            user = cursor.fetchone()

            if not verify_password(user['password_hash'], current_password):
                conn.close()
                return jsonify({'error': 'Current password is incorrect'}), HTTPStatus.UNAUTHORIZED

            # Update password
            new_password_hash = hash_password(new_password)
            cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_password_hash, request.user['id']))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Profile updated successfully',
            'username': username,
            'email': email
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password_request():
    """Request a password reset."""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({'error': 'Email is required'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get user ID
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if not user:
            # For security, don't reveal if email exists
            conn.close()
            return jsonify({'message': 'If an account exists with this email, a password reset link will be sent.'}), HTTPStatus.OK

        # Generate reset token
        token = generate_reset_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)

        # Delete old tokens for this email
        cursor.execute('DELETE FROM password_reset_tokens WHERE email = ?', (email,))

        # Create new token
        cursor.execute(
            'INSERT INTO password_reset_tokens (email, token, expires_at) VALUES (?, ?, ?)',
            (email, token, expires_at)
        )

        conn.commit()
        conn.close()

        # TODO: Send email with reset link (requires email service integration)
        # For now, we'll just store the token in a visible way for testing

        return jsonify({
            'message': 'If an account exists with this email, a password reset link has been sent.'
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/auth/reset-password-confirm', methods=['POST'])
def reset_password_confirm():
    """Confirm password reset."""
    try:
        data = request.get_json()
        token = data.get('token', '')
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')

        if not token or not password:
            return jsonify({'error': 'Token and password are required'}), HTTPStatus.BAD_REQUEST

        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), HTTPStatus.BAD_REQUEST

        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if token is valid
        cursor.execute('''
            SELECT email, created_at FROM password_reset_tokens
            WHERE token = ? AND expires_at > ?
        ''', (token, datetime.utcnow()))

        token_data = cursor.fetchone()

        if not token_data:
            conn.close()
            return jsonify({'error': 'Invalid or expired reset token'}), HTTPStatus.UNAUTHORIZED

        email = token_data['email']

        # Get user ID
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND

        # Update password
        password_hash = hash_password(password)
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user['id']))

        # Delete used token
        cursor.execute('DELETE FROM password_reset_tokens WHERE token = ?', (token,))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Password has been reset successfully'
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Create Flask app at module level
app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
