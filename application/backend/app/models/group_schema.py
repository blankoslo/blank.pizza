from app.db import db
from app.models.slack_user_schema import SlackUserSchema, SlackUserResponseSchema
from app.models.group import Group
from app.models.slack_organization_schema import SlackOrganizationSchema
from app.models.mixins import get_field

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    id = auto_field()
    name = auto_field()
    members = fields.Nested(SlackUserSchema, many=True)
    slack_organization_id = auto_field()
    slack_organization = fields.Nested(SlackOrganizationSchema, dump_only=True)


class GroupResponseSchema(GroupSchema):
    class Meta(GroupSchema.Meta):
        exclude = ("slack_organization", "slack_organization_id")

    members = fields.Nested(SlackUserResponseSchema, many=True, dump_only=True)


class GroupCreateSchema(SQLAlchemySchema):
    class Meta(GroupSchema.Meta):
        load_instance = False

    name = fields.String(required=True)
    members = fields.List(fields.String, required=True)


class GroupUpdateSchema(SQLAlchemySchema):
    class Meta(GroupSchema.Meta):
        load_instance = False

    name = fields.String(required=True)
    members = fields.List(fields.String, required=True)
