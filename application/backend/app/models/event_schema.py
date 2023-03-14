from app.db import db
from app.models.restaurant_schema import RestaurantSchema, RestaurantResponseSchema
from app.models.enums import Age, RSVP
from app.models.event import Event
from app.models.group_schema import GroupSchema, GroupResponseSchema
from app.models.mixins import get_field
from app.models.slack_organization_schema import SlackOrganizationSchema

from marshmallow import Schema, fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField


class EventSchema(SQLAlchemySchema):
    class Meta:
        model = Event
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    id = auto_field(dump_only=True)
    time = auto_field()
    restaurant_id = auto_field(load_only=True)
    restaurant = fields.Nested(RestaurantSchema, dump_only=True)
    finalized = auto_field()
    slack_organization_id = auto_field()
    slack_organization = fields.Nested(SlackOrganizationSchema, dump_only=True)
    people_per_event = auto_field()
    group_id = auto_field()
    group = fields.Nested(GroupSchema, dump_only=True)

    @validates('people_per_event')
    def validate_people_per_event(self, value):
        if value < 2:
            raise ValidationError('People per event must be at least 2')
        elif value > 100:
            raise ValidationError('People per event cannot be greater than 100')


class EventResponseSchema(EventSchema):
    class Meta(EventSchema.Meta):
        exclude = ("slack_organization", "slack_organization_id")

    restaurant = fields.Nested(RestaurantResponseSchema, dump_only=True)
    group = fields.Nested(GroupResponseSchema, dump_only=True)


class EventQueryArgsSchema(Schema):
    time = fields.DateTime(timezone=True)
    restaurant_id = fields.String()
    age = EnumField(Age, by_value=True)


class EventUpdateSchema(SQLAlchemySchema):
    class Meta(EventSchema.Meta):
        load_instance = False

    time = get_field(EventSchema, Event.time)
    restaurant_id = get_field(EventSchema, Event.restaurant_id)


class EventCreateSchema(EventSchema):
    class Meta(EventSchema.Meta):
        exclude = (
            "slack_organization",
            "slack_organization_id",
            "restaurant",
            "finalized",
            "id",
            "group",
        )
