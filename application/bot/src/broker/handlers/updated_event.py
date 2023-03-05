from src.broker.handlers import MessageHandler
from src.broker.schemas.updated_event_event import UpdatedEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector
from src.api.slack_api import SlackApi

@MessageHandler.handle('updated_event', UpdatedEventEventSchema)
def updated_event(event: dict):
    with injector.get(BotApi) as ba:
        slack_client = SlackApi(token=event['bot_token'])
        if event['is_finalized']:
            ba.inform_users_finalized_event_got_updated(
                old_time=event['old_timestamp'],
                time=event['timestamp'],
                old_restaurant_name=event['old_restaurant_name'],
                restaurant_name=event['restaurant_name'],
                slack_ids=event['slack_ids'],
                channel_id=event['channel_id'],
                slack_client=slack_client
            )
        else:
            ba.inform_users_unfinalized_event_got_updated(
                old_time=event['old_timestamp'],
                time=event['timestamp'],
                old_restaurant_name=event['old_restaurant_name'],
                restaurant_name=event['restaurant_name'],
                slack_ids=event['slack_ids'],
                slack_client=slack_client
            )

