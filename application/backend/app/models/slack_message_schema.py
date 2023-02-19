from app.db import db
from app.models.slack_message import SlackMessage

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class SlackMessageSchema(SQLAlchemySchema):
    class Meta:
        model = SlackMessage
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    ts = auto_field()
    channel_id = auto_field()
