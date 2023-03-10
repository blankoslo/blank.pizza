import requests
import json
import os
from flask import views, request, redirect, jsonify, current_app
from flask_smorest import Blueprint, abort
from app.models.user import User
from app.models.user_schema import UserSchema
from app.auth import auth
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.services.slack_organization_service import SlackOrganizationService
from app.services.injector import injector

bp = Blueprint("auth", "auth", url_prefix="/auth", description="Authentication")


def get_slack_user_info(token):
    response = requests.post("https://slack.com/api/users.identity", headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 200:
        return response.json()
    else:
        abort(400, message=f"Failed to retrieve Slack user info: {response.json()['error']}")

def get_slack_provider_cfg():
    return requests.get(current_app.config["SLACK_DISCOVERY_URL"]).json()

@bp.route("/logout")
class Auth(views.MethodView):
  def get(self):
    pass

@bp.route("/refresh")
class Auth(views.MethodView):
  @jwt_required(refresh=True)
  def post(self):
    identity = get_jwt_identity()
    user = User.get_by_id(identity)

    json_user = UserSchema().dump(user)
    additional_claims = {
        # TODO handle roles
        "user": {**json_user, "roles": []}
    }

    access_token = create_access_token(identity=user, additional_claims=additional_claims)
    return jsonify(access_token=access_token)

@bp.route("/login")
class Auth(views.MethodView):
    def get(self):
        slack_provider_cfg = get_slack_provider_cfg()
        authorization_endpoint = slack_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        base_url = os.environ.get("FRONTEND_URI").rstrip('/')
        client_id = current_app.config["SLACK_CLIENT_ID"]
        request_uri = auth.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri = f'{base_url}/login/callback',
            scope=["openid", "email", "profile"]
        )
        return jsonify({
            'auth_url': request_uri
        })

@bp.route("/login/callback")
class Auth(views.MethodView):
    def get(self):
        base_url = os.environ.get("FRONTEND_URI").rstrip('/')
        code = request.args.get("code")
        authorization_response = f'{base_url}/login/callback?'
        for key in request.args.keys():
            authorization_response += f'{key}={request.args.get(key)}&'
        slack_provider_cfg = get_slack_provider_cfg()
        token_endpoint = slack_provider_cfg["token_endpoint"]
        token_url, headers, body = auth.client.prepare_token_request(
            token_endpoint,
            authorization_response=authorization_response,
            redirect_url=f'{base_url}/login/callback',
            client_secret=current_app.config["SLACK_CLIENT_SECRET"],
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
        )

        try:
            auth.client.parse_request_body_response(json.dumps(token_response.json()))
        except:
            return abort(401)

        userinfo_endpoint = slack_provider_cfg["userinfo_endpoint"]
        uri, headers, body = auth.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        userinfo_response_data = userinfo_response.json()

        if userinfo_response_data.get("email_verified"):
            slack_organization_service = injector.get(SlackOrganizationService)

            data = {
              "id": userinfo_response_data["sub"],
              "email": userinfo_response_data["email"],
              "picture": userinfo_response_data["picture"],
              "name": userinfo_response_data["given_name"],
              "slack_organization_id": userinfo_response_data['https://slack.com/team_id']
            }

            slack_organization = slack_organization_service.get_by_id(data["slack_organization_id"])
            if slack_organization is None:
                return abort(403, message = "slack team id not found as a registered workspace.")

            
            user = User.get_by_id(data["id"])
            if user is None:
                user = UserSchema().load(data=data)
                user.upsert(user)
            
            json_user = UserSchema().dump(user)
            additional_claims = {
                # TODO handle roles
                "user": {**json_user, "roles": []}
            }
            access_token = create_access_token(identity=user, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user, additional_claims=additional_claims)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        return abort(401, message = "User email not available or not verified by Slack.")
