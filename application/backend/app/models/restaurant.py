import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship
from sqlalchemy import func, select
from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.rating import Rating

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
