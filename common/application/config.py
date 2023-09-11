# common.application.config.py

import os
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True
    if os.environ.get('DOCKER_CONTAINER') is not None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////data/database.db'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'echo': True,
    # }
     # RabbitMQ broker URL
    CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
    CELERY_RESULT_BACKEND = 'rpc://'

    broker_connection_retry_on_startup = True

    # Schedule the task to run every Sunday at midnight
    beat_schedule = {
        'calculate-weekly-profits': {
            'task': 'cron.papertrades.interactive.calculate_weekly_profits_task',
            'schedule': crontab(minute='*'),  # Run every minute
        },
    }

    # 'schedule': crontab(minute=0),  # Run at the beginning of every hour
