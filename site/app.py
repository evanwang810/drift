"""Flask application for the repository website with authentication and premium content."""

from flask import Flask, render_template, jsonify, request, session, make_response
from functools import wraps
import secrets
from datetime import datetime, timedelta
from pathlib import Path

from user_database import UserDatabase
from password_manager import PasswordManager

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

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

# Premium content protection decorator
def require_premium(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if route requires premium
        request_path = request.path
        if not request_path.startswith('/premium'):
            return f(*args, **kwargs)

        # Check if user is authenticated
        if 'user_id' not in session:
            return jsonify({
                'error': 'Premium content requires authentication',
                'premium_required': True
            }), 401

        # Get user from database
        user_id = session['user_id']
        user = user_db.get_user(user_id)

        if not user:
            return jsonify({
                'error': 'User not found',
                'premium_required': True
            }), 404

        # Check user subscription status
        if user.get('subscription_status') != 'premium':
            return jsonify({
                'error': 'Premium content requires a premium subscription',
                'premium_required': True
            }), 403

        # Check if subscription is active
        if user.get('subscription_expires_at'):
            expires_at = datetime.fromisoformat(user['subscription_expires_at'])
            if expires_at < datetime.utcnow():
                return jsonify({
                    'error': 'Premium subscription has expired',
                    'premium_required': True
                }), 403

        return f(*args, **kwargs)

    return decorated_function

# Routes
@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/login')
def login():
    """Login page."""
    return render_template('auth-login.html')

@app.route('/register')
def register():
    """Register page."""
    return render_template('auth-register.html')

@app.route('/forgot-password')
def forgot_password():
    """Forgot password page."""
    return render_template('auth-forgot-password.html')

@app.route('/profile')
def profile():
    """User profile page (requires auth)."""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401

    user_id = session['user_id']
    user = user_db.get_user(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return render_template('auth-profile.html', user=user)

@app.route('/premium')
@require_premium
def premium():
    """Premium content page (requires premium subscription)."""
    return render_template('premium.html')

@app.route('/premium/signup')
def premium_signup():
    """Premium signup page (guests can see plans)."""
    return render_template('auth-premium-signup.html')

# API Endpoints (from auth_app.py)
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
    user_id = session_data['user_id']

    # Update email if provided
    if 'email' in data:
        if user_db.email_exists(data['email']) and user_db.get_user_by_email(data['email'])['user_id'] != user_id:
            return jsonify({'error': 'Email already registered'}), 409
        user_db.update_user_email(user_id, data['email'])

    # Update username if provided
    if 'username' in data:
        if user_db.user_exists(data['username']) and user_db.get_user_by_username(data['username'])['user_id'] != user_id:
            return jsonify({'error': 'Username already taken'}), 409
        user_db.update_user_username(user_id, data['username'])

    # Update password if provided
    if 'new_password' in data and data['new_password']:
        if not password_manager.verify_password(data.get('old_password', ''), user_db.get_user(user_id)['password_hash']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        user_db.update_user_password(user_id, data['new_password'])

    return jsonify({'message': 'Profile updated successfully'})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({'authenticated': False})

    session_data = user_db.get_session(session_id)
    if not session_data or not session_data.get('is_valid'):
        return jsonify({'authenticated': False})

    user_id = session_data['user_id']
    user = user_db.get_user(user_id)

    if not user:
        return jsonify({'authenticated': False})

    return jsonify({
        'authenticated': True,
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email'],
        'subscription_status': user.get('subscription_status', 'free'),
        'subscription_expires_at': user.get('subscription_expires_at')
    })

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Request password reset."""
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    # Check if user exists
    user = user_db.get_user_by_email(email)
    if not user:
        # Don't reveal if email exists for security
        return jsonify({'message': 'If an account exists with this email, you will receive reset instructions'}), 200

    # Generate reset token
    reset_token = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    user_db.create_password_reset(reset_token, user['user_id'], expires_at)

    # Here you would normally send an email with the reset token
    # For now, we'll store it in the database for demo purposes
    return jsonify({'message': 'Password reset instructions sent to your email'}), 200

@app.route('/api/auth/reset-password/confirm', methods=['POST'])
def reset_password_confirm():
    """Confirm password reset with token."""
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('new_password', '')

    if not token:
        return jsonify({'error': 'Reset token is required'}), 400

    if not new_password or len(new_password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    # Validate token
    reset_data = user_db.get_password_reset(token)
    if not reset_data or not reset_data.get('is_valid'):
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    user_id = reset_data['user_id']
    user_db.update_user_password(user_id, new_password)
    user_db.delete_password_reset(token)

    return jsonify({'message': 'Password reset successful. You can now login with your new password'})

# Premium routes
@app.route('/premium/plan', methods=['GET'])
def premium_plan():
    """View premium plan details."""
    return render_template('premium-plans.html')

@app.route('/api/premium/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to premium plan."""
    data = request.get_json()
    plan_type = data.get('plan', 'monthly')

    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({'error': 'Authentication required'}), 401

    session_data = user_db.get_session(session_id)
    if not session_data or not session_data.get('is_valid'):
        return jsonify({'error': 'Invalid session'}), 401

    user_id = session_data['user_id']
    user = user_db.get_user(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Calculate subscription duration
    if plan_type == 'monthly':
        duration = timedelta(days=30)
    elif plan_type == 'yearly':
        duration = timedelta(days=365)
    else:
        return jsonify({'error': 'Invalid plan type'}), 400

    # Calculate expiration date
    expires_at = datetime.utcnow() + duration

    # Update user subscription
    user_db.update_user_subscription(user_id, 'premium', expires_at.isoformat())

    return jsonify({
        'message': 'Premium subscription activated successfully',
        'subscription_status': 'premium',
        'subscription_expires_at': expires_at.isoformat()
    })

@app.route('/api/premium/cancel', methods=['POST'])
def cancel_subscription():
    """Cancel premium subscription."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({'error': 'Authentication required'}), 401

    session_data = user_db.get_session(session_id)
    if not session_data or not session_data.get('is_valid'):
        return jsonify({'error': 'Invalid session'}), 401

    user_id = session_data['user_id']
    user = user_db.get_user(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Cancel subscription (set to free)
    user_db.update_user_subscription(user_id, 'free', None)

    return jsonify({'message': 'Premium subscription cancelled successfully'})

# Protected content routes
@app.route('/premium/content')
@require_premium
def premium_content():
    """Protected premium content page."""
    return render_template('premium-content.html')

@app.route('/premium/protected')
@require_premium
def protected_content():
    """Another protected content page."""
    return render_template('premium-protected.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
