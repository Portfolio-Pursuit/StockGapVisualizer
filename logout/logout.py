# logout/logout.py
from flask import Blueprint, redirect, session

logout_blueprint = Blueprint('logout', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@logout_blueprint.route('/')
def logout():
    # Clear the authentication status from the session
    session.pop('authenticated', None)
    return redirect('/login')