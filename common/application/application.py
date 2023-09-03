# papertrades.models.papertrades.py

from flask import Flask
from common.application.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Initialize the database
db = SQLAlchemy(app)

from papertrades.models.papertrades import *

with app.app_context():
    db.create_all()