# app.py
from flask import Flask
from flask_caching import Cache


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})  # Cache for 1 hour


# Import and register blueprints here
from dashboard.dashboard import dashboard_blueprint
from chart.chart import chart_blueprint
from heatmap.heatmap import heatmap_blueprint
from login.login import login_blueprint
from logout.logout import logout_blueprint
from splash.splash import splash_blueprint

# Register blueprints with the app
app.register_blueprint(login_blueprint, url_prefix='/login')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
app.register_blueprint(chart_blueprint, url_prefix='/chart')
app.register_blueprint(heatmap_blueprint, url_prefix='/heatmap')
app.register_blueprint(logout_blueprint, url_prefix='/logout')
app.register_blueprint(splash_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
    
