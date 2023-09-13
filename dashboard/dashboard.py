# dashboard.dashboard.py
from flask import Blueprint
from common.auth.login_required import login_required
from common.ui.navbar import navbar, getUIDir
from cron.papertrades.interactive.calculate_weekly_profits_task import calculate_weekly_profits_task
from common.application.application import celery

renderEnv = navbar(getUIDir(__file__)).getEnv()
dashboard_blueprint = Blueprint('dashboard', __name__, static_folder='static', static_url_path='assets')
local_template = 'dashboard.html'

@dashboard_blueprint.route('/')
@login_required
def dashboard():
    #calculate_weekly_profits_task.delay()
    #calculate_weekly_profits_task.apply_async()

    return renderEnv.get_template(local_template).render()
