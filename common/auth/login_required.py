# common.auth.login_required.py

from flask import session, redirect, url_for
from functools import wraps

# Custom decorator to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function