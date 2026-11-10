"""
Authentication Blueprint for Flask application.
Handles user registration, login, logout, password reset, and profile management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
from functools import wraps

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Import site modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site'))
from user_database import UserDatabase
from password_manager import PasswordManager

# Initialize database
user_db = UserDatabase()

# Initialize password manager
password_manager = PasswordManager()

# Premium content routes
premium_routes = Blueprint('premium', __name__, url_prefix='/premium')
premium_routes.config = {'premium': True}


def require_auth(f):
    """Decorator to require authentication for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def require_premium(f):
    """Decorator to require premium membership for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        if session.get('premium_expires', 0) < datetime.datetime.now().timestamp():
            return redirect(url_for('auth.premium', plan='upgrade'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        # Validation
        if not username or not email or not password:
            return render_template('auth-register.html',
                                  messages=[{'type': 'error', 'text': 'All fields are required'}])

        if password != confirmPassword:
            return render_template('auth-register.html',
                                  messages=[{'type': 'error', 'text': 'Passwords do not match'}])

        if len(password) < 8:
            return render_template('auth-register.html',
                                  messages=[{'type': 'error', 'text': 'Password must be at least 8 characters'}])

        # Check if username exists
        if user_db.get_user_by_username(username):
            return render_template('auth-register.html',
                                  messages=[{'type': 'error', 'text': 'Username already exists'}])

        # Check if email exists
        if user_db.get_user_by_email(email):
            return render_template('auth-register.html',
                                  messages=[{'type': 'error', 'text': 'Email already registered'}])

        # Hash password and create user
        password_hash = password_manager.hash_password(password)
        user_id = user_db.create_user(username, email, password_hash)

        if user_id:
            return redirect(url_for('auth.login', registered=True))
        else:
            return render_template('auth-register.html',
                                  messages=[{'type': 'error', 'text': 'Registration failed. Please try again.'}])

    registered = request.args.get('registered') == 'true'
    messages = request.args.getlist('messages') if registered else []
    return render_template('auth-register.html', messages=messages)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('auth-login.html',
                                  messages=[{'type': 'error', 'text': 'Username and password are required'}])

        # Get user
        user = user_db.get_user_by_username(username)

        if not user:
            return render_template('auth-login.html',
                                  messages=[{'type': 'error', 'text': 'Invalid username or password'}])

        # Verify password
        if not password_manager.verify_password(password, user['password_hash']):
            return render_template('auth-login.html',
                                  messages=[{'type': 'error', 'text': 'Invalid username or password'}])

        # Set session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['email'] = user['email']
        session['premium'] = user.get('premium', False)
        session['premium_expires'] = user.get('premium_expires', 0)

        # Redirect to next page or home
        next_page = request.args.get('next', url_for('index'))
        return redirect(next_page)

    registered = request.args.get('registered') == 'true'
    messages = request.args.getlist('messages') if registered else []
    return render_template('auth-login.html', messages=messages)


@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    """Handle password reset request."""
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            return render_template('auth-password-reset.html',
                                  messages=[{'type': 'error', 'text': 'Email is required'}])

        # Check if user exists
        user = user_db.get_user_by_email(email)

        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            reset_expires = datetime.datetime.now() + datetime.timedelta(hours=1)

            # Store token in database
            user_db.create_reset_token(user['id'], token, reset_expires.timestamp())

            # TODO: Send email with reset link (implementation depends on email service)

        # Always show success message (security best practice)
        return render_template('auth-password-reset.html',
                              messages=[{'type': 'success', 'text': 'If an account exists with this email, a password reset link has been sent.'}])

    return render_template('auth-password-reset.html')


@auth_bp.route('/reset-password-confirm', methods=['POST'])
def reset_password_confirm():
    """Handle password reset confirmation."""
    token = request.form.get('token')
    newPassword = request.form.get('newPassword')
    confirmNewPassword = request.form.get('confirmNewPassword')

    if not token or not newPassword:
        return render_template('auth-password-reset-confirm.html',
                              messages=[{'type': 'error', 'text': 'Invalid reset link. Please request a new password reset.'}])

    if newPassword != confirmNewPassword:
        return render_template('auth-password-reset-confirm.html',
                              messages=[{'type': 'error', 'text': 'Passwords do not match'}])

    if len(newPassword) < 8:
        return render_template('auth-password-reset-confirm.html',
                              messages=[{'type': 'error', 'text': 'Password must be at least 8 characters'}])

    # Validate token and reset password
    user_id = user_db.validate_reset_token(token)

    if not user_id:
        return render_template('auth-password-reset-confirm.html',
                              messages=[{'type': 'error', 'text': 'Invalid or expired reset link. Please request a new password reset.'}])

    # Hash new password
    password_hash = password_manager.hash_password(newPassword)

    # Update password
    if user_db.update_password(user_id, password_hash):
        return render_template('auth-password-reset-confirm.html',
                              messages=[{'type': 'success', 'text': 'Password reset successful! You can now login with your new password.'}])
    else:
        return render_template('auth-password-reset-confirm.html',
                              messages=[{'type': 'error', 'text': 'Failed to reset password. Please try again.'}])


@auth_bp.route('/profile', methods=['GET', 'POST'])
@require_auth
def profile():
    """Handle user profile management."""
    user_id = session['user_id']

    if request.method == 'POST':
        # Update profile
        new_username = request.form.get('username')
        new_email = request.form.get('email')

        if new_username and new_username != session['username']:
            if user_db.get_user_by_username(new_username):
                return render_template('auth-profile.html',
                                      messages=[{'type': 'error', 'text': 'Username already exists'}],
                                      user=user_db.get_user_by_id(user_id))

        if new_email and new_email != session['email']:
            if user_db.get_user_by_email(new_email):
                return render_template('auth-profile.html',
                                      messages=[{'type': 'error', 'text': 'Email already registered'}],
                                      user=user_db.get_user_by_id(user_id))

        if user_db.update_user(user_id, new_username, new_email):
            session['username'] = new_username or session['username']
            session['email'] = new_email or session['email']
            messages = [{'type': 'success', 'text': 'Profile updated successfully'}]
        else:
            messages = [{'type': 'error', 'text': 'Failed to update profile'}]

        return render_template('auth-profile.html', messages=messages, user=user_db.get_user_by_id(user_id))

    return render_template('auth-profile.html', user=user_db.get_user_by_id(user_id))


@auth_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """Handle password change."""
    user_id = session['user_id']
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Validate current password
    user = user_db.get_user_by_id(user_id)
    if not password_manager.verify_password(current_password, user['password_hash']):
        return jsonify({'success': False, 'message': 'Current password is incorrect'})

    if len(new_password) < 8:
        return jsonify({'success': False, 'message': 'New password must be at least 8 characters'})

    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})

    # Update password
    password_hash = password_manager.hash_password(new_password)
    if user_db.update_password(user_id, password_hash):
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to change password'})


@auth_bp.route('/premium', methods=['GET', 'POST'])
@require_auth
def premium():
    """Premium membership page."""
    user_id = session['user_id']
    user = user_db.get_user_by_id(user_id)

    # Check if user is already premium
    if user.get('premium', False) and user.get('premium_expires', 0) > datetime.datetime.now().timestamp():
        return render_template('auth-premium.html', user=user, premium=True, messages=[])

    if request.method == 'POST':
        plan = request.form.get('plan', 'monthly')

        if plan == 'monthly':
            # Generate subscription key
            subscription_key = f"PREM-{user['username']}-{secrets.token_urlsafe(16)}"
            premium_expires = datetime.datetime.now() + datetime.timedelta(days=30)
            price = 9.99
        elif plan == 'annual':
            subscription_key = f"PREM-{user['username']}-{secrets.token_urlsafe(16)}"
            premium_expires = datetime.datetime.now() + datetime.timedelta(days=365)
            price = 99.99
        else:
            return render_template('auth-premium.html',
                                  user=user,
                                  messages=[{'type': 'error', 'text': 'Invalid subscription plan'}])

        # Update user with premium status
        if user_db.update_premium(user_id, True, premium_expires.timestamp(), subscription_key):
            session['premium'] = True
            session['premium_expires'] = premium_expires.timestamp()
            messages = [{'type': 'success', 'text': f'Subscription activated! You now have Premium access for {plan}. Price: ${price}'}]
        else:
            messages = [{'type': 'error', 'text': 'Failed to activate subscription'}]

        return render_template('auth-premium.html', user=user, premium=True, messages=messages)

    return render_template('auth-premium.html', user=user, premium=False, messages=[])


# Premium content routes (require authentication and premium membership)
@premium_routes.route('/')
@require_auth
@require_premium
def index():
    """Premium content home page."""
    return render_template('premium/index.html')


@premium_routes.route('/documents')
@require_auth
@require_premium
def documents():
    """Premium documents page."""
    return render_template('premium/documents.html')


@premium_routes.route('/downloads')
@require_auth
@require_premium
def downloads():
    """Premium downloads page."""
    return render_template('premium/downloads.html')


@premium_routes.route('/api/dashboard')
@require_auth
@require_premium
def dashboard_api():
    """API endpoint for premium dashboard data."""
    user_id = session['user_id']
    user = user_db.get_user_by_id(user_id)

    return jsonify({
        'username': user['username'],
        'email': user['email'],
        'premium': True,
        'premium_expires': datetime.datetime.fromtimestamp(user.get('premium_expires', 0)).isoformat() if user.get('premium') else None,
        'subscription_key': user.get('subscription_key', ''),
        'plan': 'monthly' if user.get('premium_expires', 0) > datetime.datetime.now().timestamp() else None
    })
