from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
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

@scheduler.scheduled_job('interval', id='clean_up_invitations', minutes=15, jitter=120)
def clean_up_invitations():
    logger = injector.get(logging.Logger)
    logger.info("cleaning up invitations on finished events on scheduled task")
    with injector.get(BotApi) as ba:
        ba.clean_up_invitations()

@scheduler.scheduled_job('interval', id='sync_users_from_organizations', hours=6)
def sync_users_from_organizations():
    logger = injector.get(logging.Logger)
    logger.info("Syncing db with slack on scheduled task")
    with injector.get(BotApi) as ba:
        ba.sync_users_from_organizations()
