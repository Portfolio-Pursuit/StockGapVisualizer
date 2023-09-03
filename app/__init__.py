from flask import Flask

# Import and register blueprints here
from login.login import login_blueprint
from dashboard import dashboard_blueprint
from chart import chart_blueprint
from heatmap import heatmap_blueprint

# from config import Config, create_app(config_class=Config)

def create_app():
    app = Flask(__name__)
    # app.config.from_object(config_class)

    # Initialize Flask extensions here


    # Register blueprints with the app
    app.register_blueprint(login_blueprint, url_prefix='/login')
    # app.register_blueprint(dashboard_blueprint)
    # app.register_blueprint(chart_blueprint)
    # app.register_blueprint(heatmap_blueprint)

    # Register blueprints here
    return app