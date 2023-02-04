import logging

from app.services.broker import BrokerService
from app.services.broker.handlers.message_handler import MessageHandler
from app.services.broker.schemas.update_invitation import UpdateInvitationRequestSchema, UpdateInvitationResponseSchema
from app.services.broker.schemas.update_slack_user import UpdateSlackUserRequestSchema, UpdateSlackUserResponseSchema

from app.services.injector import injector
from app.services.invitation_service import InvitationService
from app.services.slack_user_service import SlackUserService

@MessageHandler.handle('update_invitation')
def update_invitation(payload: dict, correlation_id: str, reply_to: str):
    logger = injector.get(logging.Logger)
    invitation_service = injector.get(InvitationService)
    schema = UpdateInvitationRequestSchema()
    request = schema.load(payload)
    slack_id = request.get('slack_id')
    event_id = request.get('event_id')
    update_data = request.get('update_data')

    result = False
    if "reminded_at" in update_data:
        response = invitation_service.update_reminded_at(event_id, slack_id, update_data["reminded_at"].isoformat())
        result = True if response is not None else False
        logger.info("Updated reminded_at for (%s,%s)", event_id, slack_id)

    # Update invitation to either accepted or declined
    if 'rsvp' in update_data:
        response = invitation_service.update_invitation_status(event_id, slack_id, update_data["rsvp"])
        result = True if response is not None else False
        logger.info("Updated rsvp for (%s,%s)", event_id, slack_id)

    response_schema = UpdateInvitationResponseSchema()
    response = response_schema.load({'success': result})

    BrokerService.respond(response, reply_to, correlation_id)

@MessageHandler.handle('update_slack_user')
def update_slack_user(payload: dict, correlation_id: str, reply_to: str):
    logger = injector.get(logging.Logger)
    slack_user_service = injector.get(SlackUserService)
    schema = UpdateSlackUserRequestSchema()
    request = schema.load(payload)
    slack_id = request['slack_id']
    update_data = request['update_data']

    response = True
    try:
        result = slack_user_service.update(slack_id, {
            'current_username': update_data['current_username'],
            'email': update_data['email']
        })
        if result is None:
            slack_user_service.add({
                'slack_id': slack_id,
                'current_username': update_data['current_username'],
                'email': update_data['email']
            })
    except Exception as e:
        logger.warning(e)
        response = False

    response_schema = UpdateSlackUserResponseSchema()
    response = response_schema.load({'success': response})

    BrokerService.respond(response, reply_to, correlation_id)
