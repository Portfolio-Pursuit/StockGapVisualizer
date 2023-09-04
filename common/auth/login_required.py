# common.auth.login_required.py

from flask import session, redirect, url_for
from functools import wraps
from common.application.application import login_manager
from login.models.user import User
from flask_login import current_user

# Custom decorator to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login.login'))  
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    # Implement this function to return a User object by user_id
    return User.query.get(int(user_id))