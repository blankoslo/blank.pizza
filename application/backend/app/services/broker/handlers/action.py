from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.FinalizeEventIfPossible import FinalizeEventIfPossibleRequestSchema, FinalizeEventIfPossibleResponseSchema

from app.models.event import Event
from app.models.event_schema import EventSchema
from app.models.invitation import Invitation
from app.models.restaurant import Restaurant

@MessageHandler.handle('finalize_event_if_complete')
def finalize_event_if_complete(payload: dict, correlation_id: str, reply_to: str):
    schema = FinalizeEventIfPossibleRequestSchema()
    request = schema.load(payload)
    people_per_event = request.get('people_per_event')

    event_ready_to_finalize = Event.get_event_ready_to_finalize(people_per_event)

    response_data = {
        "success": True
    }

    if event_ready_to_finalize is not None:
        # Get Restaurant
        restaurant = Restaurant.get_by_id(event_ready_to_finalize.restaurant_id)

        # Update event to be finalized
        update_data = {
            'finalized': True
        }
        updated_invitation = EventSchema().load(data=update_data, instance=event_ready_to_finalize, partial=True)
        Event.upsert(updated_invitation)

        # Set response data
        internal_data = {
            'event_id': event_ready_to_finalize.id,
            'timestamp': event_ready_to_finalize.time.isoformat(),
            'restaurant_name': restaurant.name,
            'slack_ids': [user[0] for user in Invitation.get_attending_users(event_ready_to_finalize.id)]
        }
        response_data['data'] = internal_data
    else:
        response_data['success'] = False

    response_schema = FinalizeEventIfPossibleResponseSchema()
    response = response_schema.load(response_data)

    MessageHandler.respond(response, reply_to, correlation_id)
