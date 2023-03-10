from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.slack_user import SlackUser
from app.models.slack_organization_schema import SlackOrganizationSchema

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class SlackUserSchema(SQLAlchemySchema):
    class Meta:
        model = SlackUser
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    slack_id = auto_field()
    current_username = auto_field()
    first_seen = auto_field()
    active = auto_field()
    priority = auto_field()
    email = auto_field()
    slack_organization_id = auto_field()
    slack_organization = fields.Nested(SlackOrganizationSchema, dump_only=True)


class SlackUserResponseSchema(SlackUserSchema):
    class Meta(SlackUserSchema.Meta):
        exclude = ("slack_organization", "slack_organization_id")


class SlackUserUpdateSchema(SQLAlchemySchema):
    class Meta(SlackUserSchema.Meta):
        load_instance = False

    priority = auto_field()
    active = auto_field()


class SlackUserQueryArgsSchema(Schema):
    current_username = get_field(SlackUserSchema, SlackUser.current_username)
    active = get_field(SlackUserSchema, SlackUser.active)
    email = get_field(SlackUserSchema, SlackUser.email)
