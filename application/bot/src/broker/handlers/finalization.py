from src.broker.handlers import MessageHandler
from src.broker.schemas.finalization_event_event import FinalizationEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector
from src.api.slack_api import SlackApi

@MessageHandler.handle('finalization', FinalizationEventEventSchema)
def withdraw_invitation(event: dict):
    with injector.get(BotApi) as ba:
        slack_client = SlackApi(token=event['bot_token'])
        if event['is_finalized']:
            ba.send_event_finalized(
                timestamp=event['timestamp'],
                restaurant_name=event['restaurant_name'],
                slack_ids=event['slack_ids'],
                channel_id=event["channel_id"],
                slack_client=slack_client
            )
        else:
            ba.send_event_unfinalized(
                timestamp=event['timestamp'],
                restaurant_name=event['restaurant_name'],
                slack_ids=event['slack_ids'],
                channel_id=event["channel_id"],
                slack_client=slack_client
            )
