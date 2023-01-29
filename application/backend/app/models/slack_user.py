import sqlalchemy as sa
import math
from datetime import datetime
from sqlalchemy.sql import func, exists
from sqlalchemy.orm import aliased
from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.event import Event
from app.models.invitation import Invitation
from app.models.enums import RSVP

class SlackUser(CrudMixin, db.Model):
    __tablename__ = "slack_users"
    slack_id = sa.Column(sa.String, primary_key=True)
    current_username = sa.Column(sa.String, nullable=False)
    first_seen = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=func.now())
    active = sa.Column(sa.Boolean, nullable=False, server_default='t')
    priority = sa.Column(sa.Integer, nullable=False, server_default='1')
    email = sa.Column(sa.String, nullable=True)
    __table_args__ = (
        sa.CheckConstraint(priority >= 1, name='check_priority_range_min'),
        sa.CheckConstraint(priority <= 10, name='check_priority_range_max'),
    )

    @classmethod
    def get_users_to_invite(cls, number_of_users_to_invite, event_id, total_number_of_employees, employees_per_event, session=db.session):
        number_of_events_regarded = math.ceil(
          total_number_of_employees / employees_per_event)

        AliasInvitation = aliased(Invitation)

        subquery_join = session.query(Event.id)\
            .filter(
                sa.and_(
                    Event.time < datetime.now(),
                    Event.finalized == True
                )
            )\
            .order_by(Event.time.desc())\
            .limit(number_of_events_regarded)
        subquery_filter = session.query(AliasInvitation)\
            .filter(
                sa.and_(
                    AliasInvitation.event_id == event_id,
                    AliasInvitation.slack_id == cls.slack_id
                )
            )\

        query = session.query(cls.slack_id)\
            .join(
                Invitation,
                sa.and_(
                    cls.slack_id == Invitation.slack_id,
                    sa.and_(
                        Invitation.rsvp == RSVP.attending,
                        Invitation.event_id.in_(subquery_join)
                    )
                ),
                isouter = True
            )\
            .filter(
                sa.and_(
                    ~subquery_filter.exists(),
                    cls.active == True
                )
            )\
            .group_by(cls.slack_id)\
            .order_by(func.count(Invitation.rsvp), func.random())\
            .limit(number_of_users_to_invite)
        return query.all()

    def __repr__(self):
      return "<SlackUsers(id={self.id!r})".format(self=self)
