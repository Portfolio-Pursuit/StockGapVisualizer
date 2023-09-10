# app.py
from __future__ import absolute_import
from common.application.application import app

# Import and register blueprints here
from dashboard.dashboard import dashboard_blueprint
from chart.chart import chart_blueprint
from heatmap.heatmap import heatmap_blueprint
from login.login import login_blueprint
from logout.logout import logout_blueprint
from splash.splash import splash_blueprint
from papertrades.papertrades import paper_trading_blueprint

# Register blueprints with the app
app.register_blueprint(login_blueprint, url_prefix='/login')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
app.register_blueprint(paper_trading_blueprint, url_prefix='/portfolio')
app.register_blueprint(chart_blueprint, url_prefix='/chart')
app.register_blueprint(heatmap_blueprint, url_prefix='/heatmap')
app.register_blueprint(logout_blueprint, url_prefix='/logout')
app.register_blueprint(splash_blueprint, url_prefix='/')

print(app.url_map)

if __name__ == '__main__':
    app.run(port=8000)