from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.CreateInvitations import CreateInvitationsRequestSchema, CreateInvitationsResponseSchema

from app.models.invitation import Invitation
from app.models.invitation_schema import InvitationSchema

@MessageHandler.handle('create_invitations')
def create_invitations(payload: dict, correlation_id: str, reply_to: str):
    schema = CreateInvitationsRequestSchema()
    request = schema.load(payload)
    user_ids = request.get('user_ids')
    event_id = request.get('event_id')

    result = True
    try:
        for user_id in user_ids:
            invitation_schema = InvitationSchema()
            invitation = invitation_schema.load(
                data={"event_id": event_id, "slack_id": user_id},
                partial=True
            )
            Invitation.upsert(invitation)
    except Exception as e:
        print(e)
        result = False

    response_schema = CreateInvitationsResponseSchema()
    response = response_schema.load({'success': result})

    MessageHandler.respond(response, reply_to, correlation_id)
