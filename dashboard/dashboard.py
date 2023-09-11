# dashboard.dashboard.py
from flask import render_template, Blueprint, url_for
from common.auth.login_required import login_required
from .watchlist import watchlist_blueprint, watchlist_blueprint_temp
from common.application.application import app
from common.ui.navbar import navbar, getUIDir
from cron.papertrades.interactive.calculate_weekly_profits_task import calculate_weekly_profits_task
from common.application.application import celery

renderEnv = navbar(getUIDir(__file__)).getEnv()

dashboard_blueprint = Blueprint('dashboard', __name__, static_folder='static', static_url_path='assets')
local_template = 'dashboard.html'

# TODO: figure out structure but Tola likes this
app.register_blueprint(watchlist_blueprint_temp, url_prefix='/watchlist')    

dashboard_blueprint.register_blueprint(watchlist_blueprint)

@dashboard_blueprint.route('/')
@login_required
def dashboard():
    calculate_weekly_profits_task.delay()
    calculate_weekly_profits_task.apply_async()

    return renderEnv.get_template(local_template).render()
