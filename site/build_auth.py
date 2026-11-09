"""
Flask app for authentication with all routes.
"""
from flask import Flask, render_template, redirect, url_for, session, send_from_directory
from site.auth_api import auth_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'development-secret-key-change-in-production')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/premium-signup')
def premium_signup():
    return render_template('premium-signup.html')

@app.route('/premium-protected')
def premium_protected():
    if 'user_id' not in session:
        return render_template('premium-protected.html')
    return render_template('premium-protected.html')

@app.route('/premium-content')
def premium_content():
    if 'user_id' not in session:
        return render_template('premium-content.html')
    return render_template('premium-content.html')

@app.route('/templates/<path:filename>')
def serve_template(filename):
    return send_from_directory('site/templates', filename)

if __name__ == '__main__':
    print("\nStarting Flask authentication server...")
    print("Visit http://localhost:5000 to test authentication")
    app.run(host='localhost', port=5000, debug=True)
