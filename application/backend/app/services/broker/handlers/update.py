from app.services.broker.handlers import MessageHandler
from app.services.broker.schemas.UpdateInvitation import UpdateInvitationRequestSchema, UpdateInvitationResponseSchema
from app.services.broker.schemas.UpdateSlackUser import UpdateSlackUserRequestSchema, UpdateSlackUserResponseSchema
from app.services.broker.schemas.FinalizationEventEvent import FinalizationEventEventSchema

from app.models.invitation import Invitation
from app.models.slack_user import SlackUser
from app.models.slack_user_schema import SlackUserSchema
from app.models.invitation_schema import InvitationSchema
from app.models.enums import RSVP
from app.models.event import Event
from app.models.event_schema import EventSchema
from app.models.restaurant import Restaurant

def finalize_event_if_complete(event_id, people_per_event):
    event_ready_to_finalize = Event.get_event_by_id_if_ready_to_finalize(event_id, people_per_event)

    if event_ready_to_finalize is not None:
        # Update event to be finalized
        update_data = {
            'finalized': True
        }
        updated_event = EventSchema().load(data=update_data, instance=event_ready_to_finalize, partial=True)
        Event.upsert(updated_event)
        return True
    return False


@MessageHandler.handle('update_invitation')
def update_invitation(payload: dict, correlation_id: str, reply_to: str):
    schema = UpdateInvitationRequestSchema()
    request = schema.load(payload)
    slack_id = request.get('slack_id')
    event_id = request.get('event_id')
    people_per_event = request.get('people_per_event')
    update_data = request.get('update_data')

    result = True
    try:
        # Update invitation to either accepted or declined
        invitation = Invitation.get_by_id(event_id, slack_id)
        if "reminded_at" in update_data:
            update_data["reminded_at"] = update_data["reminded_at"].isoformat()
        updated_invitation = InvitationSchema().load(data=update_data, instance=invitation, partial=True)
        Invitation.upsert(updated_invitation)
        if 'rsvp' in update_data and people_per_event is not None and update_data['rsvp'] == RSVP.attending:
            # Check if event is ready to be finalized and finalize if it is
            was_finalized = finalize_event_if_complete(event_id, people_per_event)
            # Publish event that event is finalized
            if was_finalized:
                event = Event.get_by_id(event_id)
                restaurant = Restaurant.get_by_id(event.restaurant_id)
                queue_event_schema = FinalizationEventEventSchema()
                queue_event = queue_event_schema.load({
                    'is_finalized': True,
                    'event_id': event.id,
                    'timestamp': event.time.isoformat(),
                    'restaurant_name': restaurant.name,
                    'slack_ids': [user[0] for user in Invitation.get_attending_users(event.id)]
                })
                MessageHandler.publish("finalization", queue_event)
    except Exception as e:
        print(e)
        result = False

    response_schema = UpdateInvitationResponseSchema()
    response = response_schema.load({'success': result})

    MessageHandler.respond(response, reply_to, correlation_id)

@MessageHandler.handle('update_slack_user')
def update_slack_user(payload: dict, correlation_id: str, reply_to: str):
    schema = UpdateSlackUserRequestSchema()
    request = schema.load(payload)
    slack_id = request['slack_id']
    update_data = request['update_data']

    response = False
    try:
        updated_slack_user_id = SlackUserSchema().load(
            data = {
                'slack_id': slack_id,
                'current_username': update_data['current_username'],
                'email': update_data['email']
            },
            partial=True
        )
        SlackUser.upsert(updated_slack_user_id)
    except Exception as e:
        print(e)
        response = True

    response_schema = UpdateSlackUserResponseSchema()
    response = response_schema.load({'success': response})

    MessageHandler.respond(response, reply_to, correlation_id)
