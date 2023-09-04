# dashboard.dashboard.py
from flask import render_template, Blueprint
from common.auth.login_required import login_required
from .watchlist import watchlist_blueprint, watchlist_blueprint_temp
from common.application.application import app

dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='templates',
    static_folder='static', static_url_path='assets')

# TODO: figure out structure but Tola likes this
app.register_blueprint(watchlist_blueprint_temp, url_prefix='/watchlist')

dashboard_blueprint.register_blueprint(watchlist_blueprint)

@dashboard_blueprint.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')
