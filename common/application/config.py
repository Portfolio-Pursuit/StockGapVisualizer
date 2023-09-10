# common.application.config.py

import os
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # RabbitMQ broker URL
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # Schedule the task to run every Sunday at midnight
    beat_schedule = {
        'calculate-weekly-profits': {
            'task': 'celery.papertrades.interactive.calculate_weekly_profits_task',
            'schedule': crontab(minute=0),  # Run at the beginning of every hour
        },
    }