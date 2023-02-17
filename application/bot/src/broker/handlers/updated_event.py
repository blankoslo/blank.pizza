from src.broker.handlers import MessageHandler
from src.broker.schemas.updated_event_event import UpdatedEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector

@MessageHandler.handle('updated_event', UpdatedEventEventSchema)
def updated_event(event: dict):
    with injector.get(BotApi) as ba:
        if event['is_finalized']:
            ba.inform_users_finalized_event_got_updated(event['old_timestamp'], event['timestamp'], event['old_restaurant_name'], event['restaurant_name'], event['slack_ids'])
        else:
            ba.inform_users_unfinalized_event_got_updated(event['old_timestamp'], event['timestamp'], event['old_restaurant_name'], event['restaurant_name'], event['slack_ids'])

