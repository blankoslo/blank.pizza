from src.broker.handlers import MessageHandler
from src.broker.schemas.FinalizationEventEvent import FinalizationEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector

@MessageHandler.handle('finalization')
def withdraw_invitation(payload: dict):
    bot_api: BotApi = injector.get(BotApi)

    schema = FinalizationEventEventSchema()
    event = schema.load(payload)

    if event['is_finalized']:
        bot_api.send_event_finalized(event['timestamp'], event['restaurant_name'], event['slack_ids'])
    else:
        bot_api.send_event_unfinalized(event['timestamp'], event['restaurant_name'], event['slack_ids'])
