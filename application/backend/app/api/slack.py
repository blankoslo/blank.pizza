import requests
import os
import logging
from app.services.injector import injector
from flask import views, request, redirect, jsonify, current_app, Response
from flask_smorest import Blueprint, abort
from app.models.slack_organization_schema import SlackOrganizationSchema
from app.services.slack_organization_service import SlackOrganizationService
from app.services.broker import BrokerService
from app.services.broker.schemas.new_slack_organization_event import NewSlackOrganizationEventSchema


bp = Blueprint("slack", "slack", url_prefix="/slack", description="Slack OAUTH API")

@bp.route("/install")
class Slack(views.MethodView):
    def get(self):
        scopes = [
            'channels:read',
            'channels:history',
            'channels:join',
            'channels:manage',
            'groups:read',
            'chat:write',
            'files:read',
            'im:history',
            'im:write',
            'users:read',
            'users:read.email',
            'commands'
        ]
        frontend_base_url = os.environ.get("FRONTEND_URI").rstrip('/')
        callback_redirect_uri = f'{frontend_base_url}/slack/callback'
        client_id = current_app.config["SLACK_CLIENT_ID"]
        if client_id == None:
            return abort(500)
        base_redirect_url = "https://slack.com/oauth/v2/authorize"
        redirect_url = f'{base_redirect_url}?scope={",".join(scopes)}&client_id={client_id}&redirect_uri={callback_redirect_uri}'
        return jsonify(redirect_url=redirect_url)

@bp.route("/callback")
class Slack(views.MethodView):
    def post(self):
        logger = injector.get(logging.Logger)
        slack_organization_service = injector.get(SlackOrganizationService)
        url = "https://slack.com/api/oauth.v2.access"

        code = request.json.get('code')
        client_id = current_app.config["SLACK_CLIENT_ID"]
        client_secret = current_app.config["SLACK_CLIENT_SECRET"]
        if code is None:
            logger.info("Code is None")
            return abort(400)
        if client_id is None or client_secret is None:
            logger.warn("client_id or client_secret is None")
            return abort(500)

        data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.post(url, data=data).json()

        if not response['ok']:
            logger.error(response["error"])
            return abort(500)

        if response['is_enterprise_install']:
            logger.warn("NOT SUPPORTED: User tried to install app into enterprise workspace.")
            return abort(501)

        schema = SlackOrganizationSchema()
        schema_data = {
            'team_id': response['team']['id'],
            'team_name': response['team']['name'],
            'enterprise_id': response['enterprise']['id'] if ('enterprise' in response and response['enterprise'] is not None) else None,
            'enterprise_name': response['enterprise']['name'] if ('enterprise' in response and response['enterprise'] is not None) else None,
            'app_id': response['app_id'],
            'bot_user_id': response['bot_user_id'],
            'access_token': response['access_token']
        }
        slack_organization = schema.load(schema_data)
        slack_organization_service.upsert(slack_organization)

        BrokerService.publish("new_slack_organization_event", NewSlackOrganizationEventSchema().load({
            'team_id': schema_data['team_id'],
            'bot_token': schema_data['access_token']
        }))

        return Response(status=200)
