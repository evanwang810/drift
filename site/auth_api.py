"""
Authentication API Routes

This module provides Flask routes for:
- User registration
- User login/logout
- Password reset
- Profile management
"""

from flask import Blueprint, render_template, redirect, url_for, request, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

from user_database import get_user_db
from auth_middleware import login_required, premium_required, logout_user, verify_login, create_user_session

# Create blueprint
auth_bp = Blueprint('auth', __name__)


# Register Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm-password', '')
        terms = request.form.get('terms')

        # Validation
        if not all([username, email, password, confirm_password, terms]):
            flash('Please fill in all fields and accept the terms', 'error')
            return render_template('auth-register.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth-register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('auth-register.html')

        # Register user
        user_db = get_user_db()
        success, message = user_db.register_user(username, email, password)

        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'error')
            return render_template('auth-register.html')

    return render_template('auth-register.html')


# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        # Authenticate
        user = verify_login(username, password)

        if user:
            # Set session
            session.permanent = remember
            session['user'] = {
                'id': user['id'],
                'token': user['token']
            }

            # Update last login
            user_db = get_user_db()
            user_db.update_last_login(user['id'])

            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('auth-login.html')


# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


# Forgot Password Route
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle password reset request."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        if not email:
            flash('Please enter your email address', 'error')
            return render_template('auth-forgot-password.html')

        # Create reset token
        user_db = get_user_db()
        success, message = user_db.create_password_reset_token(email)

        if success:
            # In production, send email with reset link
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'error')
            return render_template('auth-forgot-password.html')

    return render_template('auth-forgot-password.html')


# Reset Password Route
@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Handle password reset."""
    token = request.args.get('token')

    if not token:
        flash('Invalid reset link', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm-password', '')

        # Validation
        if not all([password, confirm_password]):
            flash('Please fill in all fields', 'error')
            return render_template('auth-reset-password.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth-reset-password.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('auth-reset-password.html')

        # Reset password
        user_db = get_user_db()
        success, message = user_db.reset_password(token, password)

        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'error')
            return render_template('auth-reset-password.html')

    return render_template('auth-reset-password.html')


# Profile Route
@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Display and update user profile."""
    user_db = get_user_db()
    user = g.user

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        new_password = request.form.get('new-password', '')
        confirm_new_password = request.form.get('confirm-new-password', '')

        # Update profile
        success, message = user_db.update_profile(user['id'], username, email)

        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')

        # Change password if provided
        if new_password:
            if new_password != confirm_new_password:
                flash('New passwords do not match', 'error')
            elif len(new_password) < 8:
                flash('Password must be at least 8 characters', 'error')
            else:
                current_password = request.form.get('current-password', '')
                if not user_db.verify_password(current_password, user['password_hash']):
                    flash('Current password is incorrect', 'error')
                else:
                    user_db.update_password(user['id'], new_password)
                    flash('Password changed successfully', 'success')

        # Refresh user data
        user = g.user

    return render_template('auth-profile.html')


# Update Profile Route
@auth_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Handle profile update."""
    user_db = get_user_db()
    user = g.user

    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()

    success, message = user_db.update_profile(user['id'], username, email)

    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('auth.profile'))


# Change Password Route
@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Handle password change."""
    user_db = get_user_db()
    user = g.user

    current_password = request.form.get('current-password', '')
    new_password = request.form.get('new-password', '')
    confirm_new_password = request.form.get('confirm-new-password', '')

    if new_password != confirm_new_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('auth.profile'))

    if len(new_password) < 8:
        flash('Password must be at least 8 characters', 'error')
        return redirect(url_for('auth.profile'))

    if not user_db.verify_password(current_password, user['password_hash']):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('auth.profile'))

    user_db.update_password(user['id'], new_password)
    flash('Password changed successfully', 'success')
    return redirect(url_for('auth.profile'))


# Delete Account Route
@auth_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Handle account deletion."""
    user_db = get_user_db()
    user = g.user

    password = request.form.get('password', '')

    if not user_db.verify_password(password, user['password_hash']):
        flash('Password is incorrect', 'error')
        return redirect(url_for('auth.profile'))

    success, message = user_db.delete_user(user['id'])

    if success:
        flash(message, 'success')
        logout_user()
        return redirect(url_for('index'))
    else:
        flash(message, 'error')
        return redirect(url_for('auth.profile'))


# Premium Signup Route
@auth_bp.route('/premium-signup')
@premium_required
def premium_signup():
    """Display premium signup page."""
    user_db = get_user_db()
    user = g.user

    return render_template('premium-signup.html', user=user)
