# dashboard.models.watchlist.py

from common.application.application import db
from common.models.models import slugify
from datetime import datetime
from time import time

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='watchlist')
    asset = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    slug = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.generate_slug(self)

    def generate_slug(self, arg):
        if self.asset:
            self.slug = slugify(self.asset)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f"<Watchlist id: {self.id}, asset: {self.asset}>"
