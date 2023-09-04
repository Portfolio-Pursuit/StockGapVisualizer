# dashboard.dashboard.py
from flask import render_template, Blueprint, url_for
from common.auth.login_required import login_required
from .watchlist import watchlist_blueprint, watchlist_blueprint_temp
from common.application.application import app
import os
from jinja2 import ChoiceLoader, FileSystemLoader, Environment

full_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
common_ui_folder = os.path.join(full_path, 'common', 'ui', 'templates')
local_ui_folder = os.path.join(full_path, 'dashboard', 'templates')

loader = ChoiceLoader(
    [
        FileSystemLoader(local_ui_folder),  # Your project-specific templates
        FileSystemLoader(common_ui_folder),  # Common templates
    ]
)

jinja2_env = Environment(loader=loader)
jinja2_env.globals['url_for'] = url_for 

dashboard_blueprint = Blueprint('dashboard', __name__, static_folder='static', static_url_path='assets')
local_template = 'dashboard.html'

# TODO: figure out structure but Tola likes this
app.register_blueprint(watchlist_blueprint_temp, url_prefix='/watchlist')

dashboard_blueprint.register_blueprint(watchlist_blueprint)

@dashboard_blueprint.route('/')
@login_required
def dashboard():
    return jinja2_env.get_template(local_template).render()
