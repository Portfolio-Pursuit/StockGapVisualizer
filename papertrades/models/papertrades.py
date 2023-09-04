# papertrades.models.papertrades.py

from datetime import datetime
from common.application.application import db
from common.models.models import slugify
from time import time

class PaperTrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='paper_trades')
    asset = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    slug = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.generate_slug(self)

    def generate_slug(self, arg):
        if self.asset and self.timestamp:
            self.slug = slugify(f"{self.asset} {self.timestamp}")
        else:
            self.slug = str(int(time()))
    
    def __repr__(self):
        return f"<PaperTrade id: {self.id}, asset: {self.asset}, timestamp: {self.timestamp}>"

    
