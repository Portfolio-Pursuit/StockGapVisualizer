# dashboard.dashboard.py
from flask import Blueprint
from common.auth.login_required import login_required
from common.ui.navbar import navbar, getUIDir

renderEnv = navbar(getUIDir(__file__)).getEnv()
dashboard_blueprint = Blueprint('dashboard', __name__, static_folder='static', static_url_path='assets')
local_template = 'dashboard.html'

@dashboard_blueprint.route('/')
@login_required
def dashboard():
    return renderEnv.get_template(local_template).render()
