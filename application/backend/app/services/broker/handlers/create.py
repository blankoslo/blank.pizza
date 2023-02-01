from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.CreateInvitations import CreateInvitationsRequestSchema, CreateInvitationsResponseSchema
from app.services.broker.schemas.CreateImage import CreateImageRequestSchema, CreateImageResponseSchema

from app.models.invitation import Invitation
from app.models.invitation_schema import InvitationSchema
from app.models.image import Image
from app.models.image_schema import ImageSchema

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

@MessageHandler.handle('create_image')
def create_image(payload: dict, correlation_id: str, reply_to: str):
    schema = CreateImageRequestSchema()
    request = schema.load(payload)
    cloudinary_id = request.get('cloudinary_id')
    slack_id = request.get('slack_id')
    title = request.get('title')

    result = True
    try:
        image_schema = ImageSchema()
        image = image_schema.load(
            data={
                "cloudinary_id": cloudinary_id,
                "uploaded_by_id": slack_id,
                "title": title
            },
            partial=True
        )
        Image.upsert(image)
    except Exception as e:
        print(e)
        result = False

    response_schema = CreateInvitationsResponseSchema()
    response = response_schema.load({'success': result})

    MessageHandler.respond(response, reply_to, correlation_id)
