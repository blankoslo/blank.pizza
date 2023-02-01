from datetime import datetime

from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.FinalizationEventEventSchema import FinalizationEventEventSchema
from app.services.broker.schemas.WithdrawInvitation import WithdrawInvitationRequestSchema, WithdrawInvitationResponseSchema
from app.services.broker.schemas.UserWithdrewAfterFinalizationEventSchema import UserWithdrewAfterFinalizationEventSchema

from app.models.event import Event
from app.models.event_schema import EventSchema
from app.models.invitation import Invitation
from app.models.invitation_schema import InvitationSchema
from app.models.enums import RSVP
from app.models.restaurant import Restaurant

@MessageHandler.handle('withdraw_invitation')
def withdraw_invitation(payload: dict, correlation_id: str, reply_to: str):
    schema = WithdrawInvitationRequestSchema()
    request = schema.load(payload)
    event_id = request.get('event_id')
    slack_id = request.get('slack_id')

    #Check if event is in past
    result = True
    try:
        event = Event.get_by_id(event_id)
        if event.time < datetime.now():
            result = False
        else:
            # Update invitation to not attending
            invitation = Invitation.get_by_id(event_id, slack_id)
            update_data = {
                'rsvp': RSVP.not_attending
            }
            updated_invitation = InvitationSchema().load(data=update_data, instance=invitation, partial=True)
            Invitation.upsert(updated_invitation)
            if event.finalized:
                restaurant = Restaurant.get_by_id(event.restaurant_id)
                attending_users = [user[0] for user in Invitation.get_attending_users(event.id)]
                # Publish event that user withdrew after finalization
                queue_event_schema = UserWithdrewAfterFinalizationEventSchema()
                queue_event = queue_event_schema.load({
                    'event_id': event.id,
                    'timestamp': event.time,
                    'restaurant_name': restaurant.name,
                    'slack_ids': attending_users
                })
                MessageHandler.publish(queue_event)
                # Mark event as unfinalized
                update_data = {
                    'finalized': False
                }
                updated_invitation = EventSchema().load(data=update_data, instance=event, partial=True)
                Event.upsert(updated_invitation)
                # Publish event that event is unfinalized
                queue_event_schema = FinalizationEventEventSchema()
                queue_event = queue_event_schema.load({
                    'is_finalized': False,
                    'event_id': event.id,
                    'timestamp': event.time,
                    'restaurant_name': restaurant.name,
                    'slack_ids': attending_users
                })
                MessageHandler.publish(queue_event)
    except Exception as e:
        print(e)
        result = False

    response_schema = WithdrawInvitationResponseSchema()
    response = response_schema.load({'success': result})

    MessageHandler.respond(response, reply_to, correlation_id)
