# dashboard.dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from common.auth.login_required import login_required

dashboard_blueprint = Blueprint('dashboard', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@dashboard_blueprint.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')
