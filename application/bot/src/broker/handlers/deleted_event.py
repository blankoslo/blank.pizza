from src.broker.handlers import MessageHandler
from src.broker.schemas.deleted_event_event import DeletedEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector

@MessageHandler.handle('deleted_event', DeletedEventEventSchema)
def deleted_event(event: dict):
    with injector.get(BotApi) as ba:
        if event['is_finalized']:
            ba.inform_users_finalized_event_got_cancelled(event['timestamp'], event['restaurant_name'], event['slack'])
        else:
            ba.inform_users_unfinalized_event_got_cancelled(event['timestamp'], event['restaurant_name'], event['slack'])

