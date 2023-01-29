import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship
from sqlalchemy import func, select
from app.models import db
from app.models.mixins import get_field, CrudMixin
from app.models.rating import Rating

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.models.soft_delete import QueryWithSoftDelete

class Restaurant(CrudMixin, db.Model):
    __tablename__ = "restaurants"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String, nullable=False)
    link = sa.Column(sa.String, nullable=True)
    tlf = sa.Column(sa.String, nullable=True)
    address = sa.Column(sa.String, nullable=True)
    deleted = sa.Column(sa.Boolean, nullable=False, server_default='f')
    ratings = relationship("Rating", uselist=True, lazy="dynamic")

    @hybrid_property
    def rating(self):
        return self.ratings.with_entities(func.avg(Rating.rating)).scalar()

    @rating.expression
    def rating(cls):
        return (
            select(func.avg(Rating.rating))
            .where(Rating.restaurant_id == cls.id)
            .label("rating")
        )

    query_class = QueryWithSoftDelete
  
    def __repr__(self):
        return "<Restaurant(id={self.id!r})>".format(self=self)

class RestaurantSchema(SQLAlchemySchema):
    class Meta:
        model = Restaurant
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field()
    link = auto_field()
    tlf = auto_field()
    address = auto_field()
    deleted = auto_field(load_only=True)
    rating = fields.Float(dump_only=True)

class RestaurantUpdateSchema(RestaurantSchema):
    class Meta(RestaurantSchema.Meta):
        load_instance = False

    id = auto_field()
    name = get_field(RestaurantSchema, Restaurant.name)
    link = get_field(RestaurantSchema, Restaurant.link)
    tlf = get_field(RestaurantSchema, Restaurant.tlf)
    address = get_field(RestaurantSchema, Restaurant.address)

class RestaurantQueryArgsSchema(Schema):
    name = get_field(RestaurantSchema, Restaurant.name)
