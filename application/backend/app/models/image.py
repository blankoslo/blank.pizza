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

  def __repr__(self):
      return "<Image(id={self.id!r})>".format(self=self)
