from app.db import db
from app.models.restaurant_schema import RestaurantSchema
from app.models.enums import Age, RSVP
from app.models.event import Event
from app.models.mixins import get_field

from marshmallow import Schema, fields
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

class EventQueryArgsSchema(Schema):
    time = fields.DateTime(timezone=True)
    restaurant_id = fields.String()
    age = EnumField(Age, by_value=True)

class EventUpdateSchema(SQLAlchemySchema):
    class Meta(EventSchema.Meta):
        load_instance = False

    time = get_field(EventSchema, Event.time)
    restaurant_id = get_field(EventSchema, Event.restaurant_id)
