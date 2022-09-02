import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.enums import RSVP
from marshmallow_enum import EnumField
from app.models.event import EventSchema
from app.models.slack_user import SlackUserSchema

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

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

class InvitationSchema(SQLAlchemySchema):
    class Meta:
        model = Invitation
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    event_id = auto_field()
    slack_id = auto_field()
    event = fields.Nested(EventSchema, dump_only=True)
    slack_user = fields.Nested(SlackUserSchema, dump_only=True)
    invited_at = auto_field()
    rsvp = EnumField(RSVP, by_value=True)
    reminded_at = auto_field()

class InvitationUpdateSchema(SQLAlchemySchema):
    class Meta(InvitationSchema.Meta):
        load_instance = False

    rsvp = get_field(InvitationSchema, Invitation.rsvp)

class InvitationQueryArgsSchema(Schema):
    event_id = get_field(InvitationSchema, Invitation.event_id)
    slack_id = get_field(InvitationSchema, Invitation.slack_id)