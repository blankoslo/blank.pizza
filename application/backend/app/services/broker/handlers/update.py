from app.services.broker.handlers import MessageHandler
from app.services.broker.schemas.UpdateInvitation import UpdateInvitationRequestSchema, UpdateInvitationResponseSchema

from app.models.invitation import Invitation
from app.models.invitation_schema import InvitationSchema

@MessageHandler.handle('update_invitation')
def get_unanswered_invitations(payload: dict, correlation_id: str, reply_to: str):
    schema = UpdateInvitationRequestSchema()
    request = schema.load(payload)
    slack_id = request.get('slack_id')
    event_id = request.get('event_id')
    update_data = request.get('update_data')

    result = True
    try:
        invitation = Invitation.get_by_id(event_id, slack_id)
        if "reminded_at" in update_data:
            update_data["reminded_at"] = update_data["reminded_at"].isoformat()
        updated_invitation = InvitationSchema().load(data=update_data, instance=invitation, partial=True)
        Invitation.upsert(updated_invitation)
    except Exception as e:
        print(e)
        result = False

    response_schema = UpdateInvitationResponseSchema()
    response = response_schema.load({'success': result})

    MessageHandler.respond(response, reply_to, correlation_id)
