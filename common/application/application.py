# papertrades.models.papertrades.py

from flask import Flask
from common.application.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# logging handler
app.logger.setLevel(logging.INFO)  # Set the desired log level
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
app.logger.addHandler(handler)

# Initialize the database
db = SQLAlchemy()
db.url = Config.SQLALCHEMY_DATABASE_URI

login_manager = LoginManager()
login_manager.init_app(app)

from common.application.celeryconfig import *
celery = make_celery(app)

from papertrades.interactive.models.currency_interactive import *
from papertrades.interactive.models.leaderboard_interactive import *
from papertrades.interactive.models.papertrade_interactive import *
from papertrades.models.papertrades import *
from login.models.user import *

with app.app_context():
    db.init_app(app)
    db.create_all()