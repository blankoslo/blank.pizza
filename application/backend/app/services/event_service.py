import os

from app.models.event import Event
from app.models.event_schema import EventSchema

class EventService:
    def __init__(self):
        self.people_per_event = os.environ["PEOPLE_PER_EVENT"]

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

    def get_by_id(self, event_id):
        return Event.get_by_id(event_id)
