import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.enums import RSVP

class Invitation(CrudMixin, db.Model):
  __tablename__ = "invitations"
  event_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('events.id'), primary_key=True)
  slack_id = sa.Column(sa.String, sa.ForeignKey('slack_users.slack_id'), primary_key=True)
  event = relationship("Event", backref = "invitations")
  slack_user = relationship("SlackUser", backref = "invitations")
  invited_at = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=func.now())
  rsvp = sa.Column(sa.Enum(RSVP, values_callable = lambda x: [e.value for e in x]), nullable=False, server_default=RSVP.unanswered)
  reminded_at = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=func.now())

  def __repr__(self):
      return "<Invitation(id={self.id!r})>".format(self=self)
