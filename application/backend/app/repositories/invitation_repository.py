import sqlalchemy as sa
import pytz
from datetime import datetime
from sqlalchemy.sql import func
from app.db import db
from app.models.enums import RSVP
from app.models.event import Event
from app.models.invitation import Invitation
from app.models.mixins import get_field, CrudMixin


class InvitationRepository(Invitation, CrudMixin):
    @classmethod
    def get(cls, filters=None, order_by=None, page=None, per_page=None, team_id=None, session=db.session):
        query = cls.query

        if team_id:
            query = query.join(Event).filter(Event.slack_organization_id == team_id)

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
    def get_by_filter(cls, filters, team_id=None, session=db.session):
        query = cls.query

        if team_id:
            query = query.join(Event).filter(Event.slack_organization_id == team_id)

        for attr, value in filters.items():
            query = query.filter(getattr(cls, attr) == value)

        query = query.order_by(cls.invited_at.asc())
        return query.all()

    @classmethod
    def get_by_id(cls, event_id, slack_id, session=db.session):
        return cls.query.get((event_id, slack_id))

    @classmethod
    def get_attending_users(cls, event_id, session=db.session):
        query = session.query(cls.slack_id) \
            .filter(
            sa.and_(
                cls.rsvp == RSVP.attending,
                cls.event_id == event_id
            )
        ) \
            .order_by(func.random())
        return query.all()

    @classmethod
    def get_attending_or_unanswered_invitations(cls, event_id, session=db.session):
        query = session.query(cls) \
            .filter(
            sa.and_(
                sa.or_(
                    cls.rsvp == RSVP.attending,
                    cls.rsvp == RSVP.unanswered
                ),
                cls.event_id == event_id
            )
        ) \
            .order_by(func.random())
        return query.all()

    @classmethod
    def get_unanswered_invitations_on_finished_events(cls, session=db.session):
        query = session.query(cls) \
            .join(cls.event) \
            .filter(
            sa.and_(
                sa.and_(
                    cls.rsvp == RSVP.unanswered
                ),
                sa.text('events.time < :now')
            )
        ) \
            .params(now=datetime.now(pytz.utc))
        return query.all()

    @classmethod
    def add_message(cls, message, invitation, session=db.session):
        session.add(message)
        invitation.slack_message_ts = message.ts
        invitation.slack_message_channel = message.channel_id
        session.commit()
        session.refresh(message)
        session.refresh(invitation)
        return invitation
