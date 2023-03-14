from app.db import db
from sqlalchemy.dialects.postgresql import UUID

slack_user_group_association_table = db.Table('slack_user_group_association',
    db.Column('slack_user_id', db.String, db.ForeignKey('slack_users.slack_id'), primary_key=True),
    db.Column('group_id', UUID(as_uuid=True), db.ForeignKey('groups.id'), primary_key=True)
)
