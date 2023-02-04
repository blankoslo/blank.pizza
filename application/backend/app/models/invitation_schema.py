from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.enums import RSVP
from marshmallow_enum import EnumField
from app.models.event_schema import EventSchema
from app.models.slack_user_schema import SlackUserSchema
from app.models.invitation import Invitation

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

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
