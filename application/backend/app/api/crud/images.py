from flask import views
from flask_smorest import Blueprint, abort
from app.models.image import Image
from app.models.image_schema import ImageSchema, ImageQueryArgsSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("images", "images", url_prefix="/images", description="Operations on images")

@bp.route("/")
class Images(views.MethodView):
    @bp.arguments(ImageQueryArgsSchema, location="query")
    @bp.response(200, ImageSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List images"""
        total, images = Image.get(filters = args, page = pagination_parameters.page, per_page = pagination_parameters.page_size)
        pagination_parameters.item_count = total
        return images

@bp.route("/<image_id>")
class ImagesById(views.MethodView):
    @bp.response(200, ImageSchema)
    def get(self, image_id):
        """Get image by ID"""
        image = Image.get_by_id(image_id)
        if image == None:
            abort(404, message = "Image not found.")
        return image

    @bp.response(204)
    @jwt_required()
    def delete(self, image_id):
        """Delete image"""
        Image.delete(image_id)
