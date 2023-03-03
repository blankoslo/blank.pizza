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
    slack_organization_id = sa.Column(sa.String, sa.ForeignKey('slack_organizations.team_id'), nullable=True)
    slack_organization = relationship("SlackOrganization", backref="restaurants", uselist=False)

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

    @classmethod
    def get(cls, filters = None, order_by = None, page = None, per_page = None, team_id = None, session=db.session):
        query = cls.query

        if team_id:
            query = query.filter(cls.slack_organization_id == team_id)

        if filters is None:
            filters = {}
        # Add filters to the query
        for attr, value in filters.items():
            query = query.filter(getattr(cls, attr) == value)
        # Add order by to the query
        if (order_by):
            query = query.order_by(order_by())
        # If pagination is on, paginate the query
        if (page and per_page):
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            return pagination.total, pagination.items

        res = query.count(), query.all()
        return res
  
    def __repr__(self):
        return "<Restaurant(id={self.id!r})>".format(self=self)
