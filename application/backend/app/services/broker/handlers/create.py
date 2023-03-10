import logging

from app.services.broker.handlers.message_handler import MessageHandler

from app.services.broker.schemas.create_image import CreateImageRequestSchema, CreateImageResponseSchema

from app.services.injector import injector
from app.services.image_service import ImageService

@MessageHandler.handle('create_image', CreateImageRequestSchema, CreateImageResponseSchema)
def create_image(request: dict):
    logger = injector.get(logging.Logger)
    image_service = injector.get(ImageService)
    cloudinary_id = request.get('cloudinary_id')
    slack_id = request.get('slack_id')
    title = request.get('title')
    team_id = request.get('team_id')

    result = True
    try:
        image_service.add(data={
            "cloudinary_id": cloudinary_id,
            "uploaded_by_id": slack_id,
            "title": title,
        }, team_id=team_id)
    except Exception as e:
        logger.error(e)
        result = False

    return {'success': result}
