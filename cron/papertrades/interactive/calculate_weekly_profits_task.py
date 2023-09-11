from papertrades.interactive.calculate_weekly_profits import calculate_weekly_profits
from common.application.application import celery

@celery.task
def calculate_weekly_profits_task():
    calculate_weekly_profits()