from src.broker.handlers import MessageHandler
from src.broker.schemas.new_slack_organization_event import NewSlackOrganizationEventSchema
from src.api.bot_api import BotApi
from src.injector import injector
from src.api.slack_api import SlackApi


@MessageHandler.handle('new_slack_organization_event', NewSlackOrganizationEventSchema)
def new_slack_organization_event(event: dict):
    with injector.get(BotApi) as ba:
        slack_client = SlackApi(token=event['bot_token'])
        ba.welcome(slack_client=slack_client, team_id=event['team_id'])
        ba.sync_users_from_organization(team_id=event['team_id'], bot_token=event['bot_token'])


