# splash/splash.py
from flask import Blueprint, render_template

splash_blueprint = Blueprint('splash', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@splash_blueprint.route('/')
def splash():
    return render_template('splash.html')
