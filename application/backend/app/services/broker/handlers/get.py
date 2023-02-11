from app.services.broker.handlers.message_handler import MessageHandler

from app.services.broker.schemas.get_unanswered_invitations import GetUnansweredInvitationsResponseSchema, GetUnansweredInvitationsDataSchema
from app.services.broker.schemas.get_invited_unanswered_user_ids import GetInvitedUnansweredUserIdsResponseSchema

from app.models.slack_user import SlackUser
from app.models.invitation import Invitation
from app.models.enums import RSVP

@MessageHandler.handle('get_unanswered_invitations', responseSchema = GetUnansweredInvitationsResponseSchema)
def get_unanswered_invitations():
    invitations = Invitation.get_by_filter({"rsvp": RSVP.unanswered})
    response_data = [{"slack_id": invitation.slack_id, "event_id": invitation.event_id, "invited_at": invitation.invited_at.isoformat(), "reminded_at": invitation.reminded_at.isoformat() } for invitation in invitations]

    return {'invitations': response_data}

@MessageHandler.handle('get_invited_unanswered_user_ids', responseSchema = GetInvitedUnansweredUserIdsResponseSchema)
def get_unanswered_invitations():
    user_ids = SlackUser.get_invited_unanswered_user_ids()
    response_data = [user_id[0] for user_id in user_ids]

    return {'user_ids': response_data}
