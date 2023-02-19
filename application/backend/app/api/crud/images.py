from flask import views
from flask_smorest import Blueprint, abort
from app.models.image import Image
from app.models.image_schema import ImageSchema, ImageQueryArgsSchema
from flask_jwt_extended import jwt_required
from app.services.injector import injector
from app.services.image_service import ImageService

bp = Blueprint("images", "images", url_prefix="/images", description="Operations on images")

@bp.route("/")
class Images(views.MethodView):
    @bp.arguments(ImageQueryArgsSchema, location="query")
    @bp.response(200, ImageSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List images"""
        image_service = injector.get(ImageService)
        order = None
        if 'order' in args:
            order = args.pop('order')
        total, images = image_service.get(filters = args, order_by=order, page = pagination_parameters.page, per_page = pagination_parameters.page_size)
        pagination_parameters.item_count = total
        return images

@bp.route("/<image_id>")
class ImagesById(views.MethodView):
    @bp.response(200, ImageSchema)
    def get(self, image_id):
        """Get image by ID"""
        image_service = injector.get(ImageService)
        image = image_service.get_by_id(image_id)
        if image == None:
            abort(404, message = "Image not found.")
        return image

    @bp.response(204)
    @jwt_required()
    def delete(self, image_id):
        """Delete image"""
        image_service = injector.get(ImageService)
        image_service.delete(image_id)
