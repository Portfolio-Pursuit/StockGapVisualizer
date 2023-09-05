# papertrades.interactive.models.currency_interactive.py

from datetime import datetime
from common.application.application import db
from common.models.models import slugify
from time import time

class CurrencyInteractive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=lambda: initCurrency(id))
    user = db.relationship('User', back_populates='currency_interactive')
    total_currency = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    slug = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.generate_slug(self)

    def generate_slug(self, arg):
        if self.total_currency and self.created:
            self.slug = slugify(f"{self.total_currency} {self.created}")
        else:
            self.slug = str(int(time()))
    
    def __repr__(self):
        return f"<PaperTradeInteractive id: {self.id}, total_currency: {self.total_currency}, created: {self.created}>"

def initCurrency(current_user):
    initCurrencyById(current_user.id)

def initCurrencyById(current_user_id):
    paper_trade = CurrencyInteractive(
        user_id=current_user_id,
        total_currency=100000,
    )

    # Add the paper trade to the database
    db.session.add(paper_trade)
    db.session.commit()