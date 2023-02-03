provider "heroku" {
  email = var.heroku_api_email
  api_key = var.heroku_api_key
}

provider "herokux" {
  api_key = var.heroku_api_key
}
