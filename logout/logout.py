# logout.logout.py
from flask import Blueprint, redirect, url_for
from flask_login import logout_user

logout_blueprint = Blueprint('logout', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@logout_blueprint.route('/')
def logout():
    logout_user()
    return redirect(url_for('login.login')) 