from app.services.broker.handlers.message_handler import MessageHandler

from app.services.broker.schemas.get_unanswered_invitations import GetUnansweredInvitationsResponseSchema, GetUnansweredInvitationsDataSchema
from app.services.broker.schemas.get_invited_unanswered_user_ids import GetInvitedUnansweredUserIdsResponseSchema
from app.services.broker.schemas.get_slack_installation import GetSlackInstallationRequestSchema, GetSlackInstallationResponseSchema
from app.services.broker.schemas.get_slack_organizations import GetSlackOrganizationsResponseSchema

from app.services.invitation_service import InvitationService
from app.services.injector import injector

from app.models.slack_user import SlackUser
from app.models.slack_organization import SlackOrganization
from app.models.enums import RSVP

@MessageHandler.handle('get_unanswered_invitations', outgoing_schema = GetUnansweredInvitationsResponseSchema)
def get_unanswered_invitations():
    invitation_service = injector.get(InvitationService)

    invitations = invitation_service.get_by_filter("rsvp", RSVP.unanswered)
    response_data = []
    for invitation in invitations:
        data = {
            "slack_id": invitation.slack_id,
            "event_id": invitation.event_id,
            "invited_at": invitation.invited_at.isoformat(),
            "reminded_at": invitation.reminded_at.isoformat(),
        }
        if invitation.slack_message:
            data["slack_message"] = {
                "ts": invitation.slack_message.ts,
                "channel_id": invitation.slack_message.channel_id
            }
        response_data.append(data)

    return {'invitations': response_data}

@MessageHandler.handle('get_unanswered_invitations_on_finished_events_and_set_not_attending', outgoing_schema = GetUnansweredInvitationsResponseSchema)
def get_unanswered_invitations():
    invitation_service = injector.get(InvitationService)

    invitations = invitation_service.get_unanswered_invitations_on_finished_events_and_set_not_attending()
    response_data = []
    for invitation in invitations:
        data = {
            "slack_id": invitation.slack_id,
            "event_id": invitation.event_id,
            "invited_at": invitation.invited_at.isoformat(),
            "reminded_at": invitation.reminded_at.isoformat(),
        }
        if invitation.slack_message:
            data["slack_message"] = {
                "ts": invitation.slack_message.ts,
                "channel_id": invitation.slack_message.channel_id
            }
        response_data.append(data)

    return {'invitations': response_data}

@MessageHandler.handle('get_invited_unanswered_user_ids', outgoing_schema = GetInvitedUnansweredUserIdsResponseSchema)
def get_unanswered_invitations():
    user_ids = SlackUser.get_invited_unanswered_user_ids()
    response_data = [user_id[0] for user_id in user_ids]

    return {'user_ids': response_data}


@MessageHandler.handle('get_slack_installation', incoming_schema = GetSlackInstallationRequestSchema, outgoing_schema = GetSlackInstallationResponseSchema)
def get_slack_installation(request: dict):
    slack_organization = SlackOrganization.get_by_id(request['team_id'])

    response = {
        'team_id': slack_organization.team_id,
        'app_id': slack_organization.app_id,
        'bot_user_id': slack_organization.bot_user_id,
        'access_token': slack_organization.access_token
    }

    if slack_organization.team_name:
        response['team_name'] = slack_organization.team_name
    if slack_organization.enterprise_id:
        response['enterprise_id'] = slack_organization.enterprise_id
    if slack_organization.enterprise_name:
        response['enterprise_name'] = slack_organization.enterprise_name

    return response

@MessageHandler.handle('get_slack_organizations', outgoing_schema = GetSlackOrganizationsResponseSchema)
def get_slack_organizations():
    count, slack_organizations = SlackOrganization.get()
    response_data = [{
        'team_id': slack_organization.team_id,
        'bot_token': slack_organization.access_token
    } for slack_organization in slack_organizations]

    return {'organizations': response_data}
