from src.broker.handlers import MessageHandler
from src.broker.schemas.deleted_event_event import DeletedEventEventSchema
from src.api.bot_api import BotApi
from src.injector import injector
from src.api.slack_api import SlackApi

@MessageHandler.handle('deleted_event', DeletedEventEventSchema)
def deleted_event(event: dict):
    with injector.get(BotApi) as ba:
        slack_client = SlackApi(token=event['bot_token'])
        if event['is_finalized']:
            ba.inform_users_finalized_event_got_cancelled(
                time=event['timestamp'],
                restaurant_name=event['restaurant_name'],
                slack_data=event['slack'],
                channel_id=event['channel_id'],
                slack_client=slack_client
            )
        else:
            ba.inform_users_unfinalized_event_got_cancelled(
                time=event['timestamp'],
                restaurant_name=event['restaurant_name'],
                slack_data=event['slack'],
                slack_client=slack_client
            )

