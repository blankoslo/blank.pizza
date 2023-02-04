import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from app.db import db

class Rating(db.Model):
  __tablename__ = "ratings"
  slack_id = sa.Column(sa.String, sa.ForeignKey('slack_users.slack_id'), primary_key=True)
  restaurant_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('restaurants.id'), primary_key=True)
  rating = sa.Column(sa.Integer, nullable=False)
  __table_args__ = (
      sa.CheckConstraint(rating >= 1, name='check_rating_range_min'),
      sa.CheckConstraint(rating <= 5, name='check_rating_range_max'),
  )
  
  def __repr__(self):
      return "<Rating(slack_id={self.slack_id!r} restaurant_id={self.restaurant_id!r}))".format(self=self)
