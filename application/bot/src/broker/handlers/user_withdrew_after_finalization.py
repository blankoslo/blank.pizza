from src.broker.handlers import MessageHandler
from src.broker.schemas.UserWithdrewAfterFinalizationEvent import UserWithdrewAfterFinalizationEventSchema
from src.api.bot_api import BotApi
from src.injector import injector

@MessageHandler.handle('user_withdrew_after_finalization')
def withdraw_invitation(payload: dict):
    bot_api: BotApi = injector.get(BotApi)

    schema = UserWithdrewAfterFinalizationEventSchema()
    event = schema.load(payload)

    bot_api.send_user_withdrew_after_finalization(event['slack_id'], event['timestamp'], event['restaurant_name'])
