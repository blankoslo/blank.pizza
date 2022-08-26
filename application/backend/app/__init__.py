from app.db import db, migrate
from app.api import api, ma
import os

from flask import Flask
from flask_smorest import Blueprint

from app.api import events_bp, restaurants_bp, users_bp, invitations_bp, images_bp


def create_app(environment):
  # Application Init
  app = Flask(__name__)
  app.config.from_object(environment.get("base"))

  db.init_app(app)
  migrate.init_app(app, db)

  api.init_app(app)
  ma.init_app(app)

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
  api.register_blueprint(api_base_bp)