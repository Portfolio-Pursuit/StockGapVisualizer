# common.application.celeryconfig.py

from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=['cron.papertrades.interactive.calculate_weekly_profits_task']
    )
    celery.conf.update(app.config)
    return celery