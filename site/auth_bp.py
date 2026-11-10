"""
Authentication Blueprint
Implements user authentication, registration, password reset, and profile management.
"""

from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Create blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

# User database file path
USER_DB_PATH = os.path.join(os.path.dirname(__file__), 'user_database.json')

# Create user database file if it doesn't exist
if not os.path.exists(USER_DB_PATH):
    with open(USER_DB_PATH, 'w') as f:
        f.write('[]')

# Load user database
def load_users():
    """Load users from database file."""
    with open(USER_DB_PATH, 'r') as f:
        return __import__('json').load(f)

# Save user database
def save_users(users):
    """Save users to database file."""
    with open(USER_DB_PATH, 'w') as f:
        __import__('json').dump(users, f, indent=2)

# Check if user exists
def user_exists(username):
    """Check if a user with the given username exists."""
    users = load_users()
    return any(user['username'] == username for user in users)

# Check if email exists
def email_exists(email):
    """Check if a user with the given email exists."""
    users = load_users()
    return any(user['email'] == email for user in users)

# Get user by username
def get_user(username):
    """Get a user by username."""
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

# Create user
def create_user(username, email, password):
    """Create a new user."""
    users = load_users()
    new_user = {
        'username': username,
        'email': email,
        'password_hash': generate_password_hash(password),
        'joined_date': datetime.utcnow().isoformat(),
        'premium_status': 'guest',
        'premium_expires': None
    }
    users.append(new_user)
    save_users(users)
    return new_user

# Verify password
def verify_password(username, password):
    """Verify password for a user."""
    user = get_user(username)
    if not user:
        return False
    return check_password_hash(user['password_hash'], password)

# Update user password
def update_password(username, new_password):
    """Update user password."""
    users = load_users()
    for i, user in enumerate(users):
        if user['username'] == username:
            users[i]['password_hash'] = generate_password_hash(new_password)
            save_users(users)
            return True
    return False

# Check if user is premium
def is_premium(username):
    """Check if user is premium."""
    user = get_user(username)
    if not user:
        return False
    if user['premium_status'] != 'premium':
        return False
    # Check if premium has expired
    if user['premium_expires']:
        expires = datetime.fromisoformat(user['premium_expires'])
        if expires < datetime.utcnow():
            return False
    return True

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('auth-login.html', error='Username and password are required')

        if not user_exists(username):
            return render_template('auth-login.html', error='User not found')

        if not verify_password(username, password):
            return render_template('auth-login.html', error='Invalid password')

        # Set session
        session['user_id'] = username
        session['email'] = get_user(username)['email']
        session['premium_status'] = get_user(username)['premium_status']

        return redirect(url_for('auth.profile'))

    return render_template('auth-login.html')

# Register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate inputs
        if not username or not email or not password:
            return render_template('auth-register.html', error='All fields are required')

        if len(username) < 3:
            return render_template('auth-register.html', error='Username must be at least 3 characters')

        if len(password) < 8:
            return render_template('auth-register.html', error='Password must be at least 8 characters')

        if password != confirm_password:
            return render_template('auth-register.html', error='Passwords do not match')

        if user_exists(username):
            return render_template('auth-register.html', error='Username already exists')

        if email_exists(email):
            return render_template('auth-register.html', error='Email already registered')

        # Create user
        create_user(username, email, password)

        # Auto-login after registration
        session['user_id'] = username
        session['email'] = email
        session['premium_status'] = 'guest'

        return redirect(url_for('auth.profile'))

    return render_template('auth-register.html')

# Logout route
@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('auth.login'))

# Profile route
@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Display user profile."""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = get_user(session['user_id'])

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if current_password and new_password:
            if new_password != confirm_password:
                return render_template('auth-profile.html',
                    user=user,
                    error='Passwords do not match')

            if not verify_password(session['user_id'], current_password):
                return render_template('auth-profile.html',
                    user=user,
                    error='Current password is incorrect')

            update_password(session['user_id'], new_password)

        return redirect(url_for('auth.profile'))

    # Get premium expiry if applicable
    premium_expires = None
    if user['premium_status'] == 'premium' and user['premium_expires']:
        expires = datetime.fromisoformat(user['premium_expires'])
        if expires >= datetime.utcnow():
            premium_expires = expires.strftime('%Y-%m-%d')

    return render_template('auth-profile.html',
        username=user['username'],
        email=user['email'],
        premium_status=user['premium_status'],
        premium_expires=premium_expires,
        joined_date=datetime.fromisoformat(user['joined_date']).strftime('%Y-%m-%d'),
        status='Active' if user['premium_status'] == 'premium' else 'Registered')

# Password reset request route
@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Handle password reset request."""
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            return render_template('auth-password-reset.html', error='Email is required')

        users = load_users()
        user = next((u for u in users if u['email'] == email), None)

        if not user:
            # Don't reveal if email exists for security
            return render_template('auth-password-reset.html',
                success='If an account with this email exists, a reset link has been sent.')

        # In a real implementation, you would send an email with a reset token
        # For now, we'll just show a success message
        return render_template('auth-password-reset.html',
            success='If an account with this email exists, a reset link has been sent.')

    return render_template('auth-password-reset.html')

# API endpoint to check if user is premium
@auth_bp.route('/api/check-premium', methods=['GET'])
def check_premium():
    """Check if current user is premium (API endpoint)."""
    if 'user_id' not in session:
        return {'is_premium': False, 'role': 'guest'}, 401

    is_premium_user = is_premium(session['user_id'])

    return {
        'is_premium': is_premium_user,
        'role': 'premium' if is_premium_user else session.get('premium_status', 'guest')
    }

# API endpoint to upgrade to premium
@auth_bp.route('/api/upgrade-premium', methods=['POST'])
def upgrade_premium():
    """Upgrade user to premium status."""
    if 'user_id' not in session:
        return {'success': False, 'error': 'Not logged in'}, 401

    # In a real implementation, this would connect to a payment processor
    # For now, we'll just simulate upgrading
    users = load_users()
    for i, user in enumerate(users):
        if user['username'] == session['user_id']:
            users[i]['premium_status'] = 'premium'
            users[i]['premium_expires'] = (datetime.utcnow() + __import__('datetime').timedelta(days=30)).isoformat()
            save_users(users)
            break

    session['premium_status'] = 'premium'

    return {'success': True, 'message': 'Successfully upgraded to premium!'}

# API endpoint to get user info
@auth_bp.route('/api/user-info', methods=['GET'])
def get_user_info():
    """Get current user info (API endpoint)."""
    if 'user_id' not in session:
        return {'success': False, 'error': 'Not logged in'}, 401

    user = get_user(session['user_id'])

    return {
        'success': True,
        'user': {
            'username': user['username'],
            'email': user['email'],
            'premium_status': user['premium_status'],
            'joined_date': user['joined_date']
        }
    }
