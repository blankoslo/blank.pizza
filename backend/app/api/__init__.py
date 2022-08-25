# Needed for SqlAlchemy to find the class
from app.models.restaurant import Restaurant
from app.models.event import Event
from app.models.slack_user import SlackUser
from app.models.invitation import Invitation
from app.models.image import Image

from app.api.crud.invitations import bp as invitations_bp
from app.api.crud.restaurants import bp as restaurants_bp
from app.api.crud.events import bp as events_bp
from app.api.crud.images import bp as images_bp
from app.api.crud.slack_users import bp as users_bp

from flask_smorest import Api
from flask_marshmallow import Marshmallow

api = Api()
ma = Marshmallow()