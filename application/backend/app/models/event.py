from datetime import datetime
from time import timezone
import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.restaurant import RestaurantSchema
from app.models.enums import Age

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

class Event(CrudMixin, db.Model):
    __tablename__ = "events"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    time = sa.Column(sa.DateTime(timezone=True), nullable=False)
    restaurant_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('restaurants.id'), nullable=False)
    restaurant = relationship("Restaurant", backref = "events", uselist=False)
    finalized = sa.Column(sa.Boolean, nullable=False, server_default='f')

    @classmethod
    def get(cls, filters, order_by = None, page = None, per_page = None, session=db.session):
        query = session.query(cls)
        # Add filters to the query
        if ('age' in filters and filters['age'] == Age.New):
            query = query.filter(cls.time > datetime.now())
        elif ('age' in filters and filters['age'] == Age.Old):
            query = query.filter(cls.time < datetime.now())
        # Add order by to the query
        if (order_by):
            query = query.order_by(order_by())
        # If pagination is on, paginate the query
        if (page and per_page):
            pagination = query.paginate(page, per_page, False)
            return pagination.total, pagination.items
            
        res = query.count(), query.all()
        return res

    def __repr__(self):
        return "<Event(id={self.id!r})>".format(self=self)

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