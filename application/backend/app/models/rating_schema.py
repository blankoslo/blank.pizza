from app.db import db
from app.models.rating import Rating

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class RatingSchema(SQLAlchemySchema):
    class Meta:
        model = Rating
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    slack_id = auto_field()
    restaurant_id = auto_field()
    rating = auto_field()
