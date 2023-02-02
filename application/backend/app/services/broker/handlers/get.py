import os

from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.GetUnansweredInvitations import GetUnansweredInvitationsResponseSchema, GetUnansweredInvitationsDataSchema
from app.services.broker.schemas.GetInvitedUnansweredUserIds import GetInvitedUnansweredUserIdsResponseSchema

from app.models.slack_user import SlackUser
from app.models.invitation import Invitation
from app.models.enums import RSVP

@MessageHandler.handle('get_unanswered_invitations')
def get_unanswered_invitations(payload: dict, correlation_id: str, reply_to: str):
    invitations = Invitation.get_by_filter({"rsvp": RSVP.unanswered})
    response_schema = GetUnansweredInvitationsResponseSchema()
    response_data = [{"slack_id": invitation.slack_id, "event_id": invitation.event_id, "invited_at": invitation.invited_at.isoformat(), "reminded_at": invitation.reminded_at.isoformat() } for invitation in invitations]
    response = response_schema.load({'invitations': response_data})

    MessageHandler.respond(response, reply_to, correlation_id)

@MessageHandler.handle('get_invited_unanswered_user_ids')
def get_unanswered_invitations(payload: dict, correlation_id: str, reply_to: str):
    user_ids = SlackUser.get_invited_unanswered_user_ids()
    response_schema = GetInvitedUnansweredUserIdsResponseSchema()
    response_data = [user_id[0] for user_id in user_ids]
    response = response_schema.load({'user_ids': response_data})
    MessageHandler.respond(response, reply_to, correlation_id)
