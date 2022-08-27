from app.db import db, migrate
from app.api import api, ma
from app.auth import auth, jwt
import os

from flask import Flask
from flask_smorest import Blueprint
from flask_talisman import Talisman

from app.api import events_bp, restaurants_bp, users_bp, invitations_bp, images_bp, auth_bp

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
  app.secret_key = os.environ.get("SECRET_KEY")
  app.config.from_object(environment.get("base"))

  Talisman(app)

  db.init_app(app)
  migrate.init_app(app, db)

  api.init_app(app)
  ma.init_app(app)
  
  jwt.init_app(app)
  auth.init_app(app)

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