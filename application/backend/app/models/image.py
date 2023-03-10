import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db
from app.models.mixins import get_field, CrudMixin


class Image(CrudMixin, db.Model):
  __tablename__ = "images"
  cloudinary_id = sa.Column(sa.String, primary_key=True)
  uploaded_by_id = sa.Column(sa.String, sa.ForeignKey('slack_users.slack_id'), nullable=False)
  uploaded_by = relationship("SlackUser", backref ="images", uselist=False)
  uploaded_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
  title = sa.Column(sa.String)
  slack_organization_id = sa.Column(sa.String, sa.ForeignKey('slack_organizations.team_id'))

  def __repr__(self):
      return "<Image(id={self.id!r})>".format(self=self)

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
