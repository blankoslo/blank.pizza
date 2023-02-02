from src.broker.handlers import MessageHandler
from src.broker.schemas.FinalizationEventEvent import FinalizationEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector

@MessageHandler.handle('finalization')
def withdraw_invitation(payload: dict):
    schema = FinalizationEventEventSchema()
    event = schema.load(payload)

    with injector.get(BotApi) as ba:
        if event['is_finalized']:
            ba.send_event_finalized(event['timestamp'], event['restaurant_name'], event['slack_ids'])
        else:
            ba.send_event_unfinalized(event['timestamp'], event['restaurant_name'], event['slack_ids'])
