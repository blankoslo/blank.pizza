terraform {
  required_providers {
    heroku = {
      source = "heroku/heroku"
    }
    herokux = {
      source = "davidji99/herokux"
      postgres_api_url = "https://postgres-starter-api.heroku.com"
    }
  }
  required_version = ">= 0.13"
}
