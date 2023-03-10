from app.db import db
from app.models.slack_organization import SlackOrganization

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import EXCLUDE


class SlackOrganizationSchema(SQLAlchemySchema):
    class Meta:
        model = SlackOrganization
        include_relationships = True
        sqla_session = db.session
        load_instance = True
        unknown = EXCLUDE

    team_id = auto_field()
    team_name = auto_field()
    enterprise_id = auto_field()
    enterprise_name = auto_field()
    app_id = auto_field()
    bot_user_id = auto_field()
    access_token = auto_field()
