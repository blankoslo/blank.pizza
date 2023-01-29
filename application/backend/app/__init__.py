from app.db import db, migrate
from app.api import api, ma
from app.auth import auth, jwt
from app.services.broker import broker
import os
import json

from flask import Flask
from flask_smorest import Blueprint
from flask_talisman import Talisman
from flask_cors import CORS

from app.api import events_bp, restaurants_bp, users_bp, invitations_bp, images_bp, auth_bp

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

  db.init_app(app)
  migrate.init_app(app, db)

  api.init_app(app)
  ma.init_app(app)
  
  jwt.init_app(app)
  auth.init_app(app)

  def dumps_parser(data):
      return json.dumps(data, default=str)

  broker.init_app(
      app,
      'Pizza_Queue',
      json.loads,
      dumps_parser,
      #development=True
  )

  csp = {
      'default-src': ['\'self\''],
      'frame-ancestors': ['\'none\'']
  }

  Talisman(app, frame_options='DENY', content_security_policy=csp, referrer_policy='no-referrer')

  @app.after_request
  def add_headers(response):
      response.headers['X-XSS-Protection'] = '0'
      response.headers['Cache-Control'] = 'no-store, max-age=0'
      response.headers['Pragma'] = 'no-cache'
      response.headers['Expires'] = '0'
      response.headers['Content-Type'] = 'application/json; charset=utf-8'
      return response
  
  FRONTEND_URI = os.environ.get("FRONTEND_URI").rstrip('/')

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

  register_blueprints(api)

  with app.app_context():
    db.create_all()

  return app

def register_blueprints(api):
  api_base_bp = Blueprint("api", "api", url_prefix="/api", description="Api")

  api_base_bp.register_blueprint(events_bp)
  api_base_bp.register_blueprint(restaurants_bp)
  api_base_bp.register_blueprint(users_bp)
  api_base_bp.register_blueprint(invitations_bp)
  api_base_bp.register_blueprint(images_bp)
  api_base_bp.register_blueprint(auth_bp)
  api.register_blueprint(api_base_bp)
