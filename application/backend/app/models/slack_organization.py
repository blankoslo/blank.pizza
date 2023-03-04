import sqlalchemy as sa
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
