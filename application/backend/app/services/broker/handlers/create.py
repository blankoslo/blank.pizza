from app.services.broker.handlers import MessageHandler

from app.services.broker.schemas.create_image import CreateImageRequestSchema, CreateImageResponseSchema

from app.models.image import Image
from app.models.image_schema import ImageSchema

@MessageHandler.handle('create_image')
def create_image(payload: dict, correlation_id: str, reply_to: str):
    schema = CreateImageRequestSchema()
    request = schema.load(payload)
    cloudinary_id = request.get('cloudinary_id')
    slack_id = request.get('slack_id')
    title = request.get('title')

    result = True
    try:
        image_schema = ImageSchema()
        image = image_schema.load(
            data={
                "cloudinary_id": cloudinary_id,
                "uploaded_by_id": slack_id,
                "title": title
            },
            partial=True
        )
        Image.upsert(image)
    except Exception as e:
        print(e)
        result = False

    response_schema = CreateImageResponseSchema()
    response = response_schema.load({'success': result})

    MessageHandler.respond(response, reply_to, correlation_id)
