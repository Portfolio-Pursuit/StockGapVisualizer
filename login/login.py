# login.login.py
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from login.models.user import User
from flask_login import login_user
from common.application.application import db
import bcrypt

login_blueprint = Blueprint('login', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))

        error_message = 'Invalid username or password'
        return render_template('login.html', error_message=error_message)

    return render_template('login.html', error_message=None, show_registration=True)

@login_blueprint.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here (e.g., create a new user)
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            return jsonify({'error': 'Username already exists'})

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user
        new_user = User(username=username, password=hashed_password.decode('utf-8'))

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)

        return jsonify({'success': 'Registration successful'})

    # This route should only be used for POST requests
    return redirect(url_for('login.login'))