from common.application.application import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    paper_trades = db.relationship('PaperTrade', backref='owner', viewonly=True)
    paper_trades_interactive = db.relationship('PaperTradeInteractive', backref='owner', viewonly=True)
    currency_interactive = db.relationship('CurrencyInteractive', backref='owner', viewonly=True)
    watchlist = db.relationship('Watchlist,', backref = 'owner', viewonly = True )