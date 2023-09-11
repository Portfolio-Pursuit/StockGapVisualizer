from datetime import datetime
from common.application.application import db
from common.models.models import slugify
from time import time

class WeeklyLeaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='weekly_leaderboards')
    week_start_date = db.Column(db.Date, nullable=False)
    weekly_profit = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.generate_slug(self)

    def generate_slug(self, arg):
        if self.asset and self.timestamp:
            self.slug = slugify(f"{self.weekly_profit} {self.week_start_date}")
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f"<WeeklyLeaderboard id: {self.id}, user_id: {self.user_id}, week_start_date: {self.week_start_date}>"
