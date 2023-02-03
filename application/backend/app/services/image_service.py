from app.models.image import Image
from app.models.image_schema import ImageSchema

class ImageService:
    def get(self, filters, page, per_page):
        return Image.get(filters = filters, page = page, per_page = per_page)

    def get_by_id(self, image_id):
        return Image.get_by_id(image_id)

    def delete(self, image_id):
        Image.delete(image_id)

    def add(self, data):
        image_schema = ImageSchema()
        image = image_schema.load(data=data, partial=True)
        return Image.upsert(image)
