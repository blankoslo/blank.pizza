from app.db import db
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields
from app.models.user import User
from app.models.slack_organization_schema import SlackOrganizationSchema

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    id = auto_field()
    email = auto_field()
    name = auto_field()
    picture = auto_field()
    slack_organization_id = auto_field()
    slack_organization = fields.Nested(SlackOrganizationSchema, dump_only=True)
