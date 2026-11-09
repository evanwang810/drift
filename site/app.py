"""
Flask application for serving the drift website with authentication API.
"""

import os
import json
from pathlib import Path

from flask import Flask, send_from_directory, render_template, redirect, url_for, request, jsonify
from werkzeug.exceptions import NotFound

from site.build import build_all, page, POSTS, EXTENSIONS, NAV
from site.auth_api import auth_bp
from site.user_database import UserManager
from site.password_manager import PasswordManager

# Create Flask app
app = Flask(__name__, static_folder='site/static', template_folder='site/templates')

# Configure session
app.secret_key = os.getenv('SECRET_KEY', 'development-secret-key-change-in-production')

# Initialize managers
user_manager = UserManager()
password_manager = PasswordManager()

# Import blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')


# Route handlers for static pages
@app.route('/')
def index():
    """Serve the home page."""
    if not Path('docs/index.html').exists():
        return "Home page not found. Build the site first."
    return send_from_directory('docs', 'index.html')


@app.route('/runs.html')
def runs():
    """Serve the runs page."""
    if not Path('docs/runs.html').exists():
        return "Runs page not found. Build the site first."
    return send_from_directory('docs', 'runs.html')


@app.route('/tools.html')
def tools():
    """Serve the tools page."""
    if not Path('docs/tools.html').exists():
        return "Tools page not found. Build the site first."
    return send_from_directory('docs', 'tools.html')


@app.route('/metrics.html')
def metrics():
    """Serve the metrics page."""
    if not Path('docs/metrics.html').exists():
        return "Metrics page not found. Build the site first."
    return send_from_directory('docs', 'metrics.html')


@app.route('/knowledge_base.html')
def knowledge_base():
    """Serve the knowledge base page."""
    if not Path('docs/knowledge_base.html').exists():
        return "Knowledge base page not found. Build the site first."
    return send_from_directory('docs', 'knowledge_base.html')


@app.route('/search.html')
def search():
    """Serve the search page."""
    if not Path('docs/search.html').exists():
        return "Search page not found. Build the site first."
    return send_from_directory('docs', 'search.html')


@app.route('/developer_guide.html')
def developer_guide():
    """Serve the developer guide page."""
    if not Path('docs/developer_guide.html').exists():
        return "Developer guide not found. Build the site first."
    return send_from_directory('docs', 'developer_guide.html')


@app.route('/contributing.html')
def contributing():
    """Serve the contributing page."""
    if not Path('docs/contributing.html').exists():
        return "Contributing page not found. Build the site first."
    return send_from_directory('docs', 'contributing.html')


@app.route('/troubleshooting.html')
def troubleshooting():
    """Serve the troubleshooting page."""
    if not Path('docs/troubleshooting.html').exists():
        return "Troubleshooting page not found. Build the site first."
    return send_from_directory('docs', 'troubleshooting.html')


@app.route('/maintenance_checklist.html')
def maintenance_checklist():
    """Serve the maintenance checklist page."""
    if not Path('docs/maintenance_checklist.html').exists():
        return "Maintenance checklist not found. Build the site first."
    return send_from_directory('docs', 'maintenance_checklist.html')


@app.route('/feedback.html')
def feedback():
    """Serve the feedback page."""
    if not Path('docs/feedback.html').exists():
        return "Feedback page not found. Build the site first."
    return send_from_directory('docs', 'feedback.html')


@app.route('/feedback-dashboard.html')
def feedback_dashboard():
    """Serve the feedback dashboard page."""
    if not Path('docs/feedback-dashboard.html').exists():
        return "Feedback dashboard not found. Build the site first."
    return send_from_directory('docs', 'feedback-dashboard.html')


@app.route('/analytics-dashboard.html')
def analytics_dashboard():
    """Serve the analytics dashboard page."""
    if not Path('docs/analytics-dashboard.html').exists():
        return "Analytics dashboard not found. Build the site first."
    return send_from_directory('docs', 'analytics-dashboard.html')


@app.route('/authentication-data-model.html')
def authentication_data_model():
    """Serve the authentication data model page."""
    if not Path('docs/authentication-data-model.html').exists():
        return "Authentication data model page not found. Build the site first."
    return send_from_directory('docs', 'authentication-data-model.html')


@app.route('/newsletter-subscription.html')
def newsletter_subscription():
    """Serve the newsletter subscription page."""
    if not Path('docs/newsletter-subscription.html').exists():
        return "Newsletter subscription page not found. Build the site first."
    return send_from_directory('docs', 'newsletter-subscription.html')


@app.route('/quarterly-review-template.html')
def quarterly_review_template():
    """Serve the quarterly review template page."""
    if not Path('docs/quarterly-review-template.html').exists():
        return "Quarterly review template not found. Build the site first."
    return send_from_directory('docs', 'quarterly-review-template.html')


@app.route('/quarterly-review-procedure.html')
def quarterly_review_procedure():
    """Serve the quarterly review procedure page."""
    if not Path('docs/quarterly-review-procedure.html').exists():
        return "Quarterly review procedure not found. Build the site first."
    return send_from_directory('docs', 'quarterly-review-procedure.html')


@app.route('/quarterly-review-outcomes-q1-2027.html')
def quarterly_review_outcomes_q1_2027():
    """Serve the quarterly review outcomes page."""
    if not Path('docs/quarterly-review-outcomes-q1-2027.html').exists():
        return "Quarterly review outcomes page not found. Build the site first."
    return send_from_directory('docs', 'quarterly-review-outcomes-q1-2027.html')


@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    """Serve the login page or handle login POST."""
    if request.method == 'GET':
        return render_template('auth-login.html')
    elif request.method == 'POST':
        # Handle login via POST to /auth/login
        data = request.get_json()
        # This will be handled by the auth_bp blueprint
        return jsonify({'message': 'Login endpoint handled by auth_bp'}), 200


@app.route('/auth/register', methods=['GET', 'POST'])
def auth_register():
    """Serve the register page or handle registration POST."""
    if request.method == 'GET':
        return render_template('auth-register.html')
    elif request.method == 'POST':
        # Handle registration via POST to /auth/register
        data = request.get_json()
        # This will be handled by the auth_bp blueprint
        return jsonify({'message': 'Registration endpoint handled by auth_bp'}), 200


@app.route('/auth/profile', methods=['GET'])
def auth_profile():
    """Serve the profile page."""
    if not Path('docs/auth-profile.html').exists():
        return "Profile page not found. Build the site first."
    return send_from_directory('docs', 'auth-profile.html')


@app.route('/auth/logout', methods=['POST'])
def auth_logout():
    """Serve the logout page or handle logout POST."""
    if request.method == 'GET':
        return render_template('auth-login.html')
    elif request.method == 'POST':
        # This will be handled by the auth_bp blueprint
        return jsonify({'message': 'Logout endpoint handled by auth_bp'}), 200


@app.route('/auth/reset-password', methods=['GET', 'POST'])
def auth_reset_password():
    """Serve the reset password page or handle reset POST."""
    if request.method == 'GET':
        return render_template('auth-password-reset.html')
    elif request.method == 'POST':
        # Handle password reset via POST to /auth/reset-password
        data = request.get_json()
        # This will be handled by the auth_bp blueprint
        return jsonify({'message': 'Reset password endpoint handled by auth_bp'}), 200


@app.route('/auth/reset-password-confirm', methods=['GET', 'POST'])
def auth_reset_password_confirm():
    """Serve the password reset confirmation page."""
    if request.method == 'GET':
        token = request.args.get('token', '')
        return render_template('auth-password-reset-confirm.html', token=token)
    elif request.method == 'POST':
        # Handle password reset confirmation via POST to /auth/reset-password-confirm
        data = request.get_json()
        # This will be handled by the auth_bp blueprint
        return jsonify({'message': 'Reset password confirmation endpoint handled by auth_bp'}), 200


@app.route('/auth/change-password', methods=['POST'])
def auth_change_password():
    """Serve the change password page or handle change password POST."""
    if request.method == 'POST':
        # This will be handled by the auth_bp blueprint
        return jsonify({'message': 'Change password endpoint handled by auth_bp'}), 200


@app.route('/auth/verify-token', methods=['GET'])
def auth_verify_token():
    """Serve the verify token endpoint."""
    # This will be handled by the auth_bp blueprint
    return jsonify({'message': 'Verify token endpoint handled by auth_bp'}), 200


@app.route('/auth/premium', methods=['GET'])
def auth_premium():
    """Serve the check premium endpoint."""
    # This will be handled by the auth_bp blueprint
    return jsonify({'message': 'Premium check endpoint handled by auth_bp'}), 200


# API routes for authentication
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API endpoint for login."""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

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
    session_id = user_manager.create_session(user['id'])
    session_data = user_manager.get_session(session_id)

    return jsonify({
        'message': 'Login successful',
        'session_id': session_id,
        'username': user['username'],
        'email': user['email'],
        'premium': user.get('premium', False)
    }), 200


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """API endpoint for logout."""
    session_id = request.headers.get('X-Session-ID')
    if session_id:
        user_manager.end_session(session_id)

    return jsonify({'message': 'Logout successful'}), 200


@app.route('/api/auth/profile', methods=['GET'])
def api_auth_profile():
    """API endpoint for getting user profile."""
    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        return jsonify({'error': 'Not authenticated'}), 401

    user_data = user_manager.get_session(session_id)
    if not user_data:
        return jsonify({'error': 'Invalid session'}), 401

    user = user_manager.get_user_by_id(user_data['user_id'])
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


@app.route('/api/auth/change-password', methods=['POST'])
def api_change_password():
    """API endpoint for changing password."""
    session_id = request.headers.get('X-Session-ID')
    if not session_id:
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
    user_data = user_manager.get_session(session_id)
    if not user_data:
        return jsonify({'error': 'Invalid session'}), 401

    user = user_manager.get_user_by_id(user_data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Verify current password
    if not password_manager.verify_password(current_password, user['password_hash']):
        return jsonify({'error': 'Current password is incorrect'}), 401

    # Update password
    new_password_hash = password_manager.hash_password(new_password)
    user_manager.update_password(user['id'], new_password_hash)

    return jsonify({'message': 'Password changed successfully'}), 200


@app.route('/api/auth/reset-password', methods=['POST'])
def api_reset_password():
    """API endpoint for password reset."""
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


@app.route('/api/auth/reset-password-confirm', methods=['POST'])
def api_reset_password_confirm():
    """API endpoint for password reset confirmation."""
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


@app.route('/api/auth/verify-token', methods=['GET'])
def api_verify_token():
    """API endpoint for verifying authentication token."""
    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        return jsonify({'error': 'Not authenticated'}), 401

    user_data = user_manager.get_session(session_id)
    if not user_data:
        return jsonify({'error': 'Invalid session'}), 401

    user = user_manager.get_user_by_id(user_data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'authenticated': True,
        'user_id': user['id'],
        'username': user['username'],
        'premium': user.get('premium', False)
    }), 200


@app.route('/api/auth/premium', methods=['GET'])
def api_premium():
    """API endpoint for checking premium access."""
    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        return jsonify({'premium': False}), 200

    user_data = user_manager.get_session(session_id)
    if not user_data:
        return jsonify({'premium': False}), 200

    user = user_manager.get_user_by_id(user_data['user_id'])
    if not user:
        return jsonify({'premium': False}), 200

    return jsonify({'premium': user.get('premium', False)}), 200


# Serve static files
@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files."""
    return send_from_directory('site/static/css', filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files."""
    return send_from_directory('site/static/js', filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve image files."""
    return send_from_directory('site/static/images', filename)


# Build the site
@app.before_request
def build_site():
    """Build the site before serving any request."""
    build_all()


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
