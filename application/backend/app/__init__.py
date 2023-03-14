import os
import json
import logging
import sys

from app.db import db, migrate
from app.api import api, ma
from app.auth import auth, jwt
from app.services.broker import broker
from app.services.injector import injector
from app.services.invitation_service import InvitationService
from app.services.event_service import EventService
from app.services.restaurant_service import RestaurantService
from app.services.image_service import ImageService

from flask import Flask
from flask_smorest import Blueprint
from flask_talisman import Talisman
from flask_cors import CORS

from app.api import events_bp, restaurants_bp, users_bp, invitations_bp, images_bp, auth_bp, slack_bp, groups_bp

# Don't remove, needed for queue files to get imported
import app.services.broker.queue

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # TODO: Make this detect scheme from nginx/external sources, and or if we are in dev/prod
        scheme = 'https'
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

def create_app(environment):
    # Application Init
    app = Flask(__name__)
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    # Turn of redirect from /[endpoint] to /[endpoint]/ (as this gives a CORS error on preflight redirect)
    app.url_map.strict_slashes = False
    app.secret_key = os.environ.get("SECRET_KEY")
    app.config.from_object(environment.get("base"))
    FRONTEND_URI = os.environ.get("FRONTEND_URI").rstrip('/')
    # Logging for heroku
    app.logger.handlers.clear()
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
    app.logger.propagate = False
    app.logger.addHandler(logging_handler)
    app.logger.setLevel(logging.DEBUG)
    injector.binder.bind(logging.Logger, to=app.logger)

    # Set up database (sqlalchemy) and migration
    db.init_app(app)
    migrate.init_app(app, db)

    # Set up flask_smorest and flask_marshmallow
    api.init_app(app)
    ma.init_app(app)

    # Set up jwt authentication
    jwt.init_app(app)
    auth.init_app(app)

    # Set up message broker
    def dumps_parser(data):
      return json.dumps(data, default=str)

    broker.init_app(
      app,
      os.environ.get('MQ_EVENT_QUEUE'),
      json.loads,
      dumps_parser
    )

    # Set up services
    event_service = EventService()
    restaurant_service = RestaurantService()
    invitation_service = InvitationService(app.logger, event_service, restaurant_service)
    image_service = ImageService()
    injector.binder.bind(EventService, to=event_service)
    injector.binder.bind(InvitationService, to=invitation_service)
    injector.binder.bind(RestaurantService, to=restaurant_service)
    injector.binder.bind(ImageService, to=image_service)

    # Setup Talisman
    csp = {
      'default-src': ['\'self\''],
      'frame-ancestors': ['\'none\'']
    }
    Talisman(app, frame_options='DENY', content_security_policy=csp, referrer_policy='no-referrer')

    # Set up http(s) headers for added security
    @app.after_request
    def add_headers(response):
      response.headers['X-XSS-Protection'] = '0'
      response.headers['Cache-Control'] = 'no-store, max-age=0'
      response.headers['Pragma'] = 'no-cache'
      response.headers['Expires'] = '0'
      response.headers['Content-Type'] = 'application/json; charset=utf-8'
      return response

    # Set up CORS
    if app.config["ENV"] == "production":
        origins = [FRONTEND_URI]
        resources_origins = {"origins": origins}
    elif app.config["ENV"] == "development":
        origins = ["https://localhost"]
        resources_origins = {"origins": origins}
    CORS(
        app,
        resources={r"/api/*": resources_origins},
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["X-Pagination"],
        methods=["OPTIONS", "HEAD", "GET", "POST", "PUT", "PATCH", "DELETE"],
        supports_credentials=True,
        max_age=86400
    )

    # Set up / register blueprints
    register_blueprints(api)

    return app

def register_blueprints(api):
  api_base_bp = Blueprint("api", "api", url_prefix="/api", description="Api")

  api_base_bp.register_blueprint(events_bp)
  api_base_bp.register_blueprint(restaurants_bp)
  api_base_bp.register_blueprint(users_bp)
  api_base_bp.register_blueprint(invitations_bp)
  api_base_bp.register_blueprint(images_bp)
  api_base_bp.register_blueprint(auth_bp)
  api_base_bp.register_blueprint(slack_bp)
  api_base_bp.register_blueprint(groups_bp)
  api.register_blueprint(api_base_bp)
