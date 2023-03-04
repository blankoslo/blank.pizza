from src.broker.handlers import MessageHandler
from src.broker.schemas.user_withdrew_after_finalization_event import UserWithdrewAfterFinalizationEventSchema
from src.api.bot_api import BotApi
from src.injector import injector
from src.api.slack_api import SlackApi

@MessageHandler.handle('user_withdrew_after_finalization', UserWithdrewAfterFinalizationEventSchema)
def withdraw_invitation(event: dict):
    with injector.get(BotApi) as ba:
        slack_client = SlackApi(token = event['bot_token'])
        ba.send_user_withdrew_after_finalization(
            user_id=event['slack_id'],
            timestamp=event['timestamp'],
            restaurant_name=event['restaurant_name'],
            slack_client=slack_client
        )
