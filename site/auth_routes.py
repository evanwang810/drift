"""
Authentication Routes for Flask

This module provides authentication routes for registration, login, logout, and dashboard.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from user_database import get_user_db

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if g.user:
        return redirect(url_for('index'))

    user_db = get_user_db()

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')

        success, message = user_db.register_user(username, email, password)

        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if g.user:
        return redirect(url_for('index'))

    user_db = get_user_db()

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please provide username and password', 'error')
            return render_template('login.html')

        user = user_db.authenticate_user(username, password)

        if user:
            token = secrets.token_urlsafe(32)
            user_db.create_session(user['id'], token)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Handle user logout."""
    from auth_middleware import logout_user
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))


@auth_bp.route('/dashboard')
def dashboard():
    """User dashboard."""
    if not g.user:
        flash('Please login to access your dashboard', 'warning')
        return redirect(url_for('login'))

    user_db = get_user_db()
    user = user_db.get_user(g.user['id'])

    return render_template('dashboard.html', user=user)


@auth_bp.route('/premium-signup')
def premium_signup():
    """Premium subscription page."""
    if not g.user:
        flash('Please login to subscribe to premium', 'warning')
        return redirect(url_for('login'))

    return render_template('premium-signup.html')
