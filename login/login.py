# login/login.py
from flask import Blueprint, redirect, render_template, request, session, url_for

login_blueprint = Blueprint('login', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here (e.g., check credentials)
        username = request.form['username']
        password = request.form['password']
        # Example: Check if the username and password are correct
        if username == 'your_username' and password == 'your_password':
            # Store authentication status in the session
            session['authenticated'] = True
            return redirect(url_for('dashboard.dashboard'))

        # Display an error message for an incorrect login
        error_message = 'Invalid username or password'
        return render_template('login.html', error_message=error_message)

    # If it's a GET request, render the login form
    return render_template('login.html')

