import requests
import json
from flask import views, request, redirect, jsonify, current_app
from flask_smorest import Blueprint, abort
from app.models.user import User, UserSchema
from app.auth import auth
from flask_jwt_extended import create_access_token

bp = Blueprint("auth", "auth", url_prefix="/auth", description="Authentication")

def get_google_provider_cfg():
    return requests.get(current_app.config["GOOGLE_DISCOVERY_URL"]).json()

@bp.route("/login")
class Auth(views.MethodView):
    def get(self):
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        print(request.base_url + "/callback")
        request_uri = auth.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)

@bp.route("/logout")
class Auth(views.MethodView):
  def get(self):
    pass

@bp.route("/login/callback")
class Auth(views.MethodView):
    def get(self):
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = auth.client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(current_app.config["GOOGLE_CLIENT_ID"], current_app.config["GOOGLE_CLIENT_SECRET"]),
        )

        # Parse the tokens!
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
            
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token)
        return abort(400, message = "User email not available or not verified by Google.")