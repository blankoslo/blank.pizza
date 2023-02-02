from oauthlib.oauth2 import WebApplicationClient
from flask_jwt_extended import JWTManager
from app.models.user import User

class AuthClient():
  client: WebApplicationClient

  def __init__(self, app = None, **kwargs):
    if (app):
      self.client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])
  
  def init_app(self, app, **kwargs):
    self.client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"], kwargs=kwargs)

auth = AuthClient()
jwt = JWTManager()

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User.get_by_id(identity)
    return user
