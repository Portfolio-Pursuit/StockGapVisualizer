# dashboard.dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for

dashboard_blueprint = Blueprint('dashboard', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@dashboard_blueprint.route('/')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('login.login'))
    
    return render_template('dashboard.html')
