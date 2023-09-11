# papertrades.models.papertrades.py

from flask import Flask
from common.application.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Initialize the database
db = SQLAlchemy(app)
db.url = Config.SQLALCHEMY_DATABASE_URI

login_manager = LoginManager()
login_manager.init_app(app)

from common.application.celeryconfig import *
celery = make_celery(app)

from dashboard.models.watchlist_models import *
from papertrades.interactive.models.currency_interactive import *
from papertrades.interactive.models.leaderboard_interactive import *
from papertrades.interactive.models.papertrade_interactive import *
from papertrades.models.papertrades import *
from login.models.user import *

with app.app_context():
    db.create_all()