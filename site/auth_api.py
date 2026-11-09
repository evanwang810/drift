"""
Authentication API endpoints for user registration, login, password reset, and profile management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from site.user_database import UserDatabase
from site.password_manager import PasswordManager
import os
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# Initialize components
user_db = UserDatabase()
password_manager = PasswordManager()

# Configuration
TOKEN_EXPIRY_HOURS = 24
RESET_TOKEN_EXPIRY_HOURS = 1


@auth_bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'registered')

        # Validate input
        if not username or not email or not password:
            return render_template('auth-register.html', error_message='All fields are required')

        if password != confirm_password:
            return render_template('auth-register.html', error_message='Passwords do not match')

        if len(password) < 8:
            return render_template('auth-register.html', error_message='Password must be at least 8 characters')

        # Check if user already exists
        if user_db.get_user_by_username(username):
            return render_template('auth-register.html', error_message='Username already exists')

        if user_db.get_user_by_email(email):
            return render_template('auth-register.html', error_message='Email already registered')

        # Create new user
        user_id = user_db.create_user(username, email, password, role)

        # Set session
        session['user_id'] = user_id
        session['username'] = username
        session['role'] = role

        return redirect(url_for('auth.profile'))

    return render_template('auth-register.html')


@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            return render_template('auth-login.html', error_message='Username and password are required')

        # Get user
        user = user_db.get_user_by_username(username)

        if not user or not password_manager.verify_password(password, user['password_hash']):
            return render_template('auth-login.html', error_message='Invalid username or password')

        # Set session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']

        # Redirect based on role
        if user['role'] == 'premium':
            return redirect(url_for('auth.profile'))
        return redirect(url_for('home'))

    return render_template('auth-login.html')


@auth_bp.route('/auth/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/auth/profile')
def profile():
    """Display user profile."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = user_db.get_user_by_id(session['user_id'])

    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    return render_template('auth-profile.html', user=user)


@auth_bp.route('/auth/password-reset', methods=['GET', 'POST'])
def password_reset():
    """Request password reset."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        if not email:
            return render_template('auth-password-reset.html', error_message='Email is required')

        user = user_db.get_user_by_email(email)

        if user:
            # Generate reset token
            token = secrets.token_hex(32)
            expiry = datetime.utcnow() + timedelta(hours=RESET_TOKEN_EXPIRY_HOURS)

            # Store token in database
            user_db.create_password_reset_token(user['id'], token, expiry)

            # In production, send email with reset link
            # For demo, store in a simple file (not recommended for production)
            reset_file = os.path.join('site', 'temp_password_resets.txt')
            with open(reset_file, 'a') as f:
                f.write(f"{user['id']},{token},{expiry.isoformat()}\n")

        # Always show success message (security best practice - don't reveal if email exists)
        return render_template('auth-password-reset.html',
                             success_message='If the email exists, a reset link has been sent.')

    return render_template('auth-password-reset.html')


@auth_bp.route('/auth/password-reset-confirm', methods=['GET', 'POST'])
def password_reset_confirm():
    """Confirm and complete password reset."""
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_new_password = request.form.get('confirm_new_password', '')

        if not token or not new_password or not confirm_new_password:
            return render_template('auth-reset-confirm.html',
                                 error_message='All fields are required')

        if new_password != confirm_new_password:
            return render_template('auth-reset-confirm.html',
                                 error_message='Passwords do not match')

        if len(new_password) < 8:
            return render_template('auth-reset-confirm.html',
                                 error_message='Password must be at least 8 characters')

        # Verify token
        reset_data = user_db.get_password_reset_token(token)

        if not reset_data:
            return render_template('auth-reset-confirm.html',
                                 error_message='Invalid or expired reset token')

        # Check if token is expired
        expiry = datetime.fromisoformat(reset_data['expiry'])
        if datetime.utcnow() > expiry:
            return render_template('auth-reset-confirm.html',
                                 error_message='Reset token has expired')

        # Update password
        user_id = reset_data['user_id']
        new_hash = password_manager.hash_password(new_password)
        user_db.update_password(user_id, new_hash)

        # Remove token
        user_db.delete_password_reset_token(token)

        # Redirect to login
        return render_template('auth-reset-confirm.html',
                             success_message='Password reset successful. Please login with your new password.')

    return render_template('auth-reset-confirm.html')


# API endpoints for AJAX requests
@auth_bp.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated."""
    if 'user_id' in session:
        user = user_db.get_user_by_id(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            })
    return jsonify({'authenticated': False})


@auth_bp.route('/api/auth/change-password', methods=['POST'])
def change_password():
    """Change user password (requires authentication)."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_new_password = request.form.get('confirm_new_password', '')

        if not current_password or not new_password or not confirm_new_password:
            return jsonify({'error': 'All fields are required'}), 400

        if new_password != confirm_new_password:
            return jsonify({'error': 'Passwords do not match'}), 400

        if len(new_password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400

        user_id = session['user_id']
        user = user_db.get_user_by_id(user_id)

        # Verify current password
        if not password_manager.verify_password(current_password, user['password_hash']):
            return jsonify({'error': 'Current password is incorrect'}), 400

        # Update password
        new_hash = password_manager.hash_password(new_password)
        user_db.update_password(user_id, new_hash)

        return jsonify({'success': True, 'message': 'Password changed successfully'})


# Premium content protection middleware
def require_premium(f):
    """Decorator to require premium access for routes."""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        user = user_db.get_user_by_id(session['user_id'])
        if not user or user['role'] != 'premium':
            return render_template('auth-premium-required.html')
        return f(*args, **kwargs)
    return decorated_function
