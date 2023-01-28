import requests
import json
import os
from flask import views, request, redirect, jsonify, current_app
from flask_smorest import Blueprint, abort
from app.models.user import User, UserSchema
from app.auth import auth
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

bp = Blueprint("auth", "auth", url_prefix="/auth", description="Authentication")

def get_google_provider_cfg():
    return requests.get(current_app.config["GOOGLE_DISCOVERY_URL"]).json()

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
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        base_url = os.environ.get("FRONTEND_URI").rstrip('/')
        request_uri = auth.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri = f'{base_url}/login/callback',
            scope=["openid", "email", "profile"],
        )
        return jsonify({
            'auth_url': request_uri
        });

@bp.route("/login/callback")
class Auth(views.MethodView):
    def get(self):
        base_url = os.environ.get("FRONTEND_URI").rstrip('/')
        code = request.args.get("code")
        authorization_response = f'{base_url}/login/callback?'
        for key in request.args.keys():
            authorization_response += f'{key}={request.args.get(key)}&';
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = auth.client.prepare_token_request(
            token_endpoint,
            authorization_response= authorization_response,
            redirect_url= f'{base_url}/login/callback',
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(current_app.config["GOOGLE_CLIENT_ID"], current_app.config["GOOGLE_CLIENT_SECRET"]),
        )

        auth.client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = auth.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.json().get("email_verified"):
            data = {
              "id": userinfo_response.json()["sub"],
              "email": userinfo_response.json()["email"],
              "picture": userinfo_response.json()["picture"],
              "name": userinfo_response.json()["given_name"]
            }
            
            user = User.get_by_id(data["id"])
            if (not user):
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
        return abort(400, message = "User email not available or not verified by Google.")
