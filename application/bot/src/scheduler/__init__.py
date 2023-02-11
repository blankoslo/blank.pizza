from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.api.bot_api import BotApi
from src.injector import injector

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval', id='auto_reply', minutes=15, jitter=120)
def auto_reply():
    logger = injector.get(logging.Logger)
    logger.info("Auto replying on scheduled task")
    with injector.get(BotApi) as ba:
        ba.auto_reply()

@scheduler.scheduled_job('interval', id='invite_multiple_if_needed', minutes=15, jitter=120)
def invite_multiple_if_needed():
    logger = injector.get(logging.Logger)
    logger.info("Inviting multiple if need on scheduled task")
    with injector.get(BotApi) as ba:
        ba.invite_multiple_if_needed()

@scheduler.scheduled_job('interval', id='send_reminders', minutes=15, jitter=120)
def send_reminders():
    logger = injector.get(logging.Logger)
    logger.info("Sending reminders on scheduled task")
    with injector.get(BotApi) as ba:
        ba.send_reminders()

@scheduler.scheduled_job('interval', id='sync_db_with_slack', hours=6, jitter=120)
def sync_db_with_slack_and_return_count():
    logger = injector.get(logging.Logger)
    logger.info("Syncing db with slack on scheduled task")
    with injector.get(BotApi) as ba:
        ba.sync_db_with_slack_and_return_count()
