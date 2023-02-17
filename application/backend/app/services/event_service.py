import os
import pytz
from datetime import datetime

from app.models.event import Event
from app.models.invitation import Invitation
from app.models.event_schema import EventSchema
from app.services.broker.schemas.deleted_event_event import DeletedEventEventSchema
from app.services.broker import BrokerService

class EventService:
    def __init__(self):
        self.people_per_event = os.environ["PEOPLE_PER_EVENT"]

    def get_events_in_need_of_invitations(self):
        days_in_advance_to_invite = int(os.environ["DAYS_IN_ADVANCE_TO_INVITE"])
        people_per_event = int(os.environ["PEOPLE_PER_EVENT"])
        return Event.get_events_in_need_of_invitations(days_in_advance_to_invite, people_per_event)

    def finalize_event_if_complete(self, event_id):
        event_ready_to_finalize = Event.get_event_by_id_if_ready_to_finalize(event_id, self.people_per_event)

        if event_ready_to_finalize is not None:
            # Update event to be finalized
            update_data = {
                'finalized': True
            }
            updated_event = EventSchema().load(data=update_data, instance=event_ready_to_finalize, partial=True)
            Event.upsert(updated_event)
            return True
        return False

    def unfinalize_event(self, event_id):
        event = Event.get_by_id(event_id)
        update_data = {
            'finalized': False
        }
        updated_invitation = EventSchema().load(data=update_data, instance=event, partial=True)
        Event.upsert(updated_invitation)

    def get(self, filters, page, per_page):
        return Event.get(filters = filters, page = page, per_page = per_page)

    def get_by_id(self, event_id):
        return Event.get_by_id(event_id)

    def delete(self, event_id):
        event = Event.get_by_id(event_id)
        if event.time < datetime.now(pytz.utc):
            return False
        # Has to be lazy loaded before we delete event
        restaurant = event.restaurant
        attending_or_unanswered_users = [user[0] for user in Invitation.get_attending_or_unanswered_users(event.id)]

        Event.delete(event_id)

        queue_event_schema = DeletedEventEventSchema()
        queue_event = queue_event_schema.load({
            'is_finalized': event.finalized,
            'event_id': event.id,
            'timestamp': event.time.isoformat(),
            'restaurant_name': restaurant.name,
            'slack_ids': attending_or_unanswered_users
        })
        BrokerService.publish("deleted_event", queue_event)
        return True

    def add(self, data):
        return Event.upsert(data)

    def update(self, event_id, data):
        event = Event.get_by_id(event_id)
        if event.time < datetime.now(pytz.utc):
            return None
        return Event.update(event_id, data)
