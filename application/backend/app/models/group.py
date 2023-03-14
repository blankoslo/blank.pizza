from datetime import datetime, timedelta
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import db
from app.models.slack_user_group_association import slack_user_group_association_table


class Group(db.Model):
    __tablename__ = "groups"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String, nullable=False)
    slack_organization_id = sa.Column(sa.String, sa.ForeignKey('slack_organizations.team_id'), nullable=False)

    members = relationship(
        "SlackUser",
        secondary=slack_user_group_association_table,
        back_populates="groups"
    )

    def __repr__(self):
        return "<Group(id={self.id!r})>".format(self=self)

