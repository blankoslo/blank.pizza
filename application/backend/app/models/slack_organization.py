import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db import db


class SlackOrganization(db.Model):
    __tablename__ = "slack_organizations"
    team_id = sa.Column(sa.String, primary_key=True)
    team_name = sa.Column(sa.String, nullable=True)
    enterprise_id = sa.Column(sa.String, nullable=True)
    enterprise_name = sa.Column(sa.String, nullable=True)
    app_id = sa.Column(sa.String)
    bot_user_id = sa.Column(sa.String)
    access_token = sa.Column(sa.String)
    channel_id = sa.Column(sa.String, nullable=True)
    slack_users = relationship("SlackUser", backref="slack_organization", cascade="all, delete-orphan")
    users = relationship("User", backref="slack_organization", cascade="all, delete-orphan")
    events = relationship("Event", backref="slack_organization", cascade="all, delete-orphan")
    images = relationship("Image", backref="slack_organization", cascade="all, delete-orphan")
    restaurants = relationship("Restaurant", backref="slack_organization", cascade="all, delete-orphan")
    groups = relationship("Group", backref="slack_organization", cascade="all, delete-orphan")


