import logging

from app.services.broker import BrokerService
from app.services.broker.handlers.message_handler import MessageHandler

from app.services.broker.schemas.create_image import CreateImageRequestSchema, CreateImageResponseSchema

from app.services.injector import injector
from app.services.image_service import ImageService

@MessageHandler.handle('create_image')
def create_image(payload: dict, correlation_id: str, reply_to: str):
    logger = injector.get(logging.Logger)
    image_service = injector.get(ImageService)
    schema = CreateImageRequestSchema()
    request = schema.load(payload)
    cloudinary_id = request.get('cloudinary_id')
    slack_id = request.get('slack_id')
    title = request.get('title')

    result = True
    try:
        image_service.add({
            "cloudinary_id": cloudinary_id,
            "uploaded_by_id": slack_id,
            "title": title
        })
    except Exception as e:
        logger.error(e)
        result = False

    response_schema = CreateImageResponseSchema()
    response = response_schema.load({'success': result})

    BrokerService.respond(response, reply_to, correlation_id)
