from src.broker.handlers import MessageHandler
from src.broker.schemas.finalization_event_event import FinalizationEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector

@MessageHandler.handle('finalization', FinalizationEventEventSchema)
def withdraw_invitation(event: dict):
    with injector.get(BotApi) as ba:
        if event['is_finalized']:
            ba.send_event_finalized(event['timestamp'], event['restaurant_name'], event['slack_ids'], event['bot_token'])
        else:
            ba.send_event_unfinalized(event['timestamp'], event['restaurant_name'], event['slack_ids'], event['bot_token'])
