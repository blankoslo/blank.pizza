import pytz
from datetime import datetime

from app.models.invitation import Invitation
from app.models.enums import RSVP

from app.services.event_service import EventService
from app.services.restaurant_service import RestaurantService

from app.services.broker import BrokerService
from app.models.invitation_schema import InvitationSchema, InvitationUpdateSchema, InvitationQueryArgsSchema
from app.services.broker.schemas.finalization_event_event import FinalizationEventEventSchema
from app.services.broker.schemas.user_withdrew_after_finalization_event import UserWithdrewAfterFinalizationEventSchema

class InvitationService:
    def __init__(self, event_service: EventService, restaurant_service: RestaurantService):
        self.event_service = event_service
        self.restaurant_service = restaurant_service

    def get(self, filters, page, per_page):
        return Invitation.get(filters = filters, page = page, per_page = per_page)

    def get_by_filter(self, key, value):
        return Invitation.get_by_filter({key: value})

    def get_by_id(self, event_id):
        return Invitation.get_by_id(event_id)

    def update_invitation_status(self, event_id, user_id, rsvp):
        invitation = Invitation.get_by_id(event_id, user_id)

        if invitation is None:
            return None

        try:
            # If their current status is Attending, and they change it then it's a withdrawal that needs to be handled
            if invitation.rsvp == RSVP.attending:
                return self._withdraw_invitation(rsvp, invitation)
            # If they accept an invitation then we need to check if the event is to be finalized
            elif rsvp == RSVP.attending:
                return self._accept_invitation(invitation)
            # In other cases we simply update the invitation
            else:
                return self._update_invitation(
                    {'rsvp': rsvp},
                    invitation
                )
        except:
            return None

    def update_reminded_at(self, event_id, slack_id, date):
        invitation = Invitation.get_by_id(event_id, slack_id)

        if invitation is None:
            return None

        try:
            return self._update_invitation(
                {'reminded_at': date},
                invitation
            )
        except:
            return None

    def _withdraw_invitation(self, rsvp, invitation):
        event = self.event_service.get_by_id(invitation.event_id)
        if event.time < datetime.now(pytz.utc):
            return None
        else:
            # Update invitation to not attending
            updated_invitation = self._update_invitation({'rsvp': RSVP.not_attending}, invitation)
            if event.finalized:
                restaurant = self.restaurant_service.get_by_id(event.restaurant_id)
                attending_users = [user[0] for user in Invitation.get_attending_users(event.id)]
                # Publish event that user withdrew after finalization
                queue_event_schema = UserWithdrewAfterFinalizationEventSchema()
                queue_event = queue_event_schema.load({
                    'event_id': updated_invitation.event_id,
                    'slack_id': updated_invitation.slack_id,
                    'timestamp': event.time.isoformat(),
                    'restaurant_name': restaurant.name
                })
                BrokerService.publish("user_withdrew_after_finalization", queue_event)
                # Mark event as unfinalized
                self.event_service.unfinalize_event(event.id)
                # Publish event that event is unfinalized
                queue_event_schema = FinalizationEventEventSchema()
                queue_event = queue_event_schema.load({
                    'is_finalized': False,
                    'event_id': event.id,
                    'timestamp': event.time.isoformat(),
                    'restaurant_name': restaurant.name,
                    'slack_ids': attending_users
                })
                BrokerService.publish("finalization", queue_event)
            return updated_invitation

    def _accept_invitation(self, invitation):
        updated_invitation = self._update_invitation(
            {'rsvp': RSVP.attending},
            invitation
        )
        was_finalized = self.event_service.finalize_event_if_complete(invitation.event_id)
        # Publish event that event is finalized
        if was_finalized:
            event = self.event_service.get_by_id(invitation.event_id)
            restaurant = self.restaurant_service.get_by_id(event.restaurant_id)
            queue_event_schema = FinalizationEventEventSchema()
            queue_event = queue_event_schema.load({
                'is_finalized': True,
                'event_id': event.id,
                'timestamp': event.time.isoformat(),
                'restaurant_name': restaurant.name,
                'slack_ids': [user[0] for user in Invitation.get_attending_users(event.id)]
            })
            BrokerService.publish("finalization", queue_event)
        return updated_invitation

    def _update_invitation(self, update_data, invitation):
        updated_invitation = InvitationSchema().load(data=update_data, instance=invitation, partial=True)
        Invitation.upsert(updated_invitation)
        return updated_invitation
