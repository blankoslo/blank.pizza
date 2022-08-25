import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import db
from app.models.mixins import get_field, CrudMixin

from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class SlackUser(CrudMixin, db.Model):
  __tablename__ = "slack_users"
  slack_id = sa.Column(sa.String, primary_key=True)
  current_username = sa.Column(sa.String, nullable=False)
  first_seen = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=func.now())
  active = sa.Column(sa.Boolean, nullable=False, server_default='t')
  priority = sa.Column(sa.Integer, nullable=False, server_default='1')
  email = sa.Column(sa.String, nullable=True)
  __table_args__ = (
        sa.CheckConstraint(priority >= 1, name='check_priority_range_min'),
        sa.CheckConstraint(priority <= 10, name='check_priority_range_max'),
    )
  
  def __repr__(self):
      return "<SlackUsers(id={self.id!r})".format(self=self)

class SlackUserSchema(SQLAlchemySchema):
    class Meta:
        model = SlackUser
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    slack_id = auto_field()
    current_username = auto_field()
    first_seen = auto_field()
    active = auto_field()
    priority = auto_field()
    email = auto_field()

class SlackUserUpdateSchema(SQLAlchemySchema):
    class Meta(SlackUserSchema.Meta):
        load_instance = False

    priority = auto_field()
    active = auto_field()

class SlackUserQueryArgsSchema(Schema):
    current_username = get_field(SlackUserSchema, SlackUser.current_username)
    active = get_field(SlackUserSchema, SlackUser.active)
    email = get_field(SlackUserSchema, SlackUser.email)
