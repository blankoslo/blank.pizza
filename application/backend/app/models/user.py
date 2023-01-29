import sqlalchemy as sa
from app.models import db
from app.models.mixins import CrudMixin
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class User(CrudMixin, db.Model):
    __tablename__ = "users"
    id = sa.Column(db.String, primary_key=True)
    email = sa.Column(db.String, nullable=False, unique=True)
    name = sa.Column(db.String, nullable=False)
    picture = sa.Column(db.String, nullable=False)

    def __repr__(self):
      return "<User(id={self.id!r})".format(self=self)

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
