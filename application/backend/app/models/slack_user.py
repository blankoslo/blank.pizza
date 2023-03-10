import sqlalchemy as sa
import math
from datetime import datetime
from sqlalchemy.sql import func, exists
from sqlalchemy.orm import aliased, relationship
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
    ratings = relationship("Rating", backref="slack_user", cascade="all, delete-orphan")
    slack_organization_id = sa.Column(sa.String, sa.ForeignKey('slack_organizations.team_id'))
    __table_args__ = (
        sa.CheckConstraint(priority >= 1, name='check_priority_range_min'),
        sa.CheckConstraint(priority <= 10, name='check_priority_range_max'),
    )

    @classmethod
    def get(cls, filters = None, order_by = None, page = None, per_page = None, team_id = None, session=db.session):
        query = cls.query

        if team_id:
            query = query.filter(cls.slack_organization_id == team_id)

        if filters is None:
            filters = {}
        # Add filters to the query
        for attr, value in filters.items():
            query = query.filter(getattr(cls, attr) == value)
        # Add order by to the query
        if (order_by):
            query = query.order_by(order_by())
        # If pagination is on, paginate the query
        if (page and per_page):
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            return pagination.total, pagination.items

        res = query.count(), query.all()
        return res

    @classmethod
    def get_users_to_invite(cls, number_of_users_to_invite, event_id, total_number_of_employees, employees_per_event, session=db.session):
        number_of_events_regarded = math.ceil(total_number_of_employees / employees_per_event)

        AliasInvitation = aliased(Invitation)
        AliasEvent = aliased(Event)

        subquery_join = session.query(Event.id) \
            .filter(
                sa.and_(
                    Event.time < datetime.now(),
                    Event.finalized == True
                )
            ) \
            .order_by(Event.time.desc()) \
            .limit(number_of_events_regarded)
        subquery_filter = session.query(AliasInvitation) \
            .filter(
                sa.and_(
                    AliasInvitation.event_id == event_id,
                    AliasInvitation.slack_id == cls.slack_id
                )
            )
        subquery_organization = session.query(Event.slack_organization_id) \
            .filter(Event.id == event_id)

        query = session.query(cls.slack_id) \
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
            ) \
            .filter(  # Filter out those we're already invited and those who arent active, and only those in the organization of the event
                sa.and_(
                    cls.slack_organization_id == subquery_organization.scalar_subquery(),
                    sa.and_(
                        ~subquery_filter.exists(),
                        cls.active == True
                    )
                )
            ) \
            .group_by(cls.slack_id) \
            .order_by(func.count(Invitation.rsvp), func.random()) \
            .limit(number_of_users_to_invite)
        return query.all()

    @classmethod
    def get_invited_unanswered_user_ids(cls, session=db.session):
        query = session.query(cls.slack_id) \
            .join(
                Invitation,
                cls.slack_id == Invitation.slack_id
            ) \
            .filter(Invitation.rsvp == RSVP.unanswered) \
            .distinct()
        return query.all()

    def __repr__(self):
        return "<SlackUsers(id={self.id!r})".format(self=self)
