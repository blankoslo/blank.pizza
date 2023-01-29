from app.db import db
from app.models.mixins import get_field, CrudMixin
from app.models.image import Image

from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class ImageSchema(SQLAlchemySchema):
    class Meta:
        model = Image
        include_relationships = True
        sqla_session = db.session
        load_instance = True

    cloudinary_id = auto_field()
    uploaded_by_id = auto_field()
    uploaded_by = auto_field()
    uploaded_at = auto_field()
    title = auto_field()

class ImageQueryArgsSchema(Schema):
    uploaded_by_id = get_field(ImageSchema, Image.uploaded_by_id)
