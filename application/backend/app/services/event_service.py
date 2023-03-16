import os
import pytz
from datetime import datetime

from app.models.event import Event
from app.models.restaurant import Restaurant
from app.models.group import Group
from app.repositories.invitation_repository import InvitationRepository
from app.models.event_schema import EventSchema
from app.services.broker.schemas.deleted_event_event import DeletedEventEventSchema
from app.services.broker.schemas.updated_event_event import UpdatedEventEventSchema
from app.services.broker import BrokerService

class EventService:
    def get_events_in_need_of_invitations(self):
        days_in_advance_to_invite = int(os.environ["DAYS_IN_ADVANCE_TO_INVITE"])
        return Event.get_events_in_need_of_invitations(days_in_advance_to_invite=days_in_advance_to_invite)

    def finalize_event_if_complete(self, event_id):
        event_ready_to_finalize = Event.get_event_by_id_if_ready_to_finalize(event_id=event_id)

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
        event = Event.get_by_id(id=event_id)
        update_data = {
            'finalized': False
        }
        updated_invitation = EventSchema().load(data=update_data, instance=event, partial=True)
        Event.upsert(updated_invitation)

    def get(self, filters, page, per_page, team_id):
        return Event.get(filters = filters, page = page, per_page = per_page, team_id = team_id)

    def get_by_id(self, event_id, team_id = None):
        event = Event.get_by_id(id=event_id)
        if event is None or (team_id is not None and event.slack_organization_id != team_id):
            return None
        return event

    def delete(self, event_id, team_id):
        event = Event.get_by_id(id=event_id)

        if event is None or event.slack_organization_id != team_id or event.time < datetime.now(pytz.utc):
            return False

        # Has to be lazy loaded before we delete event
        restaurant = event.restaurant
        slack_organization = event.slack_organization
        invitations = InvitationRepository.get_attending_or_unanswered_invitations(event.id)
        slack_data = []
        for invitation in invitations:
            slack_data_entry = {
                'user_id': invitation.slack_id,
            }
            if invitation.slack_message:
                slack_data_entry['invitation_message'] = {
                    'ts': invitation.slack_message_ts,
                    'channel_id': invitation.slack_message_channel
                }
            slack_data.append(slack_data_entry)

        Event.delete(event_id)

        queue_event_schema = DeletedEventEventSchema()
        queue_event = queue_event_schema.load({
            'is_finalized': event.finalized,
            'event_id': event.id,
            'timestamp': event.time.isoformat(),
            'restaurant_name': restaurant.name,
            'slack': slack_data,
            'team_id': slack_organization.team_id,
            'bot_token': slack_organization.access_token,
            'channel_id': slack_organization.channel_id
        })
        BrokerService.publish("deleted_event", queue_event)
        return True

    def add(self, data, team_id):
        data.slack_organization_id = team_id

        restaurant = Restaurant.get_by_id(data.restaurant_id)

        if restaurant.slack_organization_id != team_id:
            return None

        if data.group_id is not None:
            group = Group.get_by_id(data.group_id)
            if group.slack_organization_id != team_id:
                return None

        return Event.upsert(data)

    def update(self, event_id, data, team_id):
        event = Event.get_by_id(id=event_id)

        if event is None or event.slack_organization_id != team_id or event.time < datetime.now(pytz.utc):
            return None

        old_time = event.time
        old_restaurant_name = event.restaurant.name

        updated_event = Event.update(event_id, data)

        attending_or_unanswered_users = [invitation.slack_id for invitation in InvitationRepository.get_attending_or_unanswered_invitations(event.id)]
        queue_event_schema = UpdatedEventEventSchema()
        queue_event = queue_event_schema.load({
            'is_finalized': event.finalized,
            'event_id': event.id,
            'old_timestamp': old_time.isoformat(),
            'timestamp': event.time.isoformat(),
            'old_restaurant_name': old_restaurant_name,
            'restaurant_name': event.restaurant.name,
            'slack_ids': attending_or_unanswered_users,
            'team_id': event.slack_organization_id,
            'bot_token': event.slack_organization.access_token,
            'channel_id': event.slack_organization.channel_id
        })
        BrokerService.publish("updated_event", queue_event)

        return updated_event
