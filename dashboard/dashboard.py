# dashboard.dashboard.py
from __future__ import absolute_import
from flask import render_template, Blueprint
from common.auth.login_required import login_required

api_blueprints = ['dashboard', 'watchlist']

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix= '/dashboard', template_folder='templates',
    static_folder='static', static_url_path='assets')

@dashboard_blueprint.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')
