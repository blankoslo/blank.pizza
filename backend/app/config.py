import os

class Base(object):
  SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  API_TITLE = "API"
  API_VERSION = "v1"
  # Swagger config
  OPENAPI_VERSION = "3.0.2"
  # Api json docs is available under /doc/openapi.json
  OPENAPI_URL_PREFIX = "/doc"
  # The swagger UI is displayed under /doc/swagger
  OPENAPI_SWAGGER_UI_PATH = "/swagger"
  # The following is equivalent to OPENAPI_SWAGGER_UI_VERSION = '3.19.5'
  OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/"