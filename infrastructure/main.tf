resource "heroku_pipeline" "pizzabot" {
  name = "pizzabot"
}

resource "heroku_app" "staging-backend" {
  name = "pizzabot-staging-backend"
  region = "eu"
  stack = "heroku-22"

  sensitive_config_vars = {
    "SECRET_KEY" = var.SECRET_KEY_BACKEND
    "GOOGLE_CLIENT_ID" = var.GOOGLE_CLIENT_ID
    "GOOGLE_CLIENT_SECRET" = var.GOOGLE_CLIENT_SECRET
  }
}

resource "heroku_app" "staging-bot" {
  name = "pizzabot-staging-bot"
  region = "eu"
  stack = "heroku-22"

  sensitive_config_vars = {
    "SLACK_BOT_TOKEN" = var.SLACK_BOT_TOKEN
    "SLACK_APP_TOKEN" = var.SLACK_APP_TOKEN
    "PIZZA_CHANNEL_ID" = var.PIZZA_CHANNEL_ID
  }
}

resource "heroku_config" "endpoints" {
    vars = {
        FRONTEND_URI = heroku_app.staging-frontend.web_url
        BACKEND_URI = heroku_app.staging-backend.web_url
    }
}

resource "heroku_app_config_association" "config_backend_association" {
  app_id = heroku_app.staging-backend.id

  vars = heroku_config.endpoints.vars
  sensitive_vars = heroku_config.endpoints.sensitive_vars
}

data "external" "frontend_build" {
	program = ["bash", "-c", <<EOT
((export BACKEND_URI=${heroku_app.staging-backend.web_url}; cd ../application/frontend && npm run build:production && cd ../../infrastructure)  >&2 && echo "{\"nop\": \"nop\"}")
EOT
]
  depends_on = [
    heroku_app.staging-backend
  ]
}

resource "heroku_app" "staging-frontend" {
  name = "pizzabot-staging-frontend"
  region = "eu"
  stack = "heroku-22"

  config_vars = {
    "NGINX_DEFAULT_REQUEST" = "index.html"
  }

  depends_on = [
    data.external.frontend_build
  ]
}

resource "heroku_build" "staging-backend" {
  app_id = heroku_app.staging-backend.id
  buildpacks = [
    "https://github.com/heroku/heroku-buildpack-locale",
    "https://github.com/heroku/heroku-buildpack-python"
  ]

  source {
    path = "../application/backend"
  }
}

resource "heroku_build" "staging-bot" {
  app_id = heroku_app.staging-bot.id
  buildpacks = [
    "https://github.com/heroku/heroku-buildpack-locale",
    "https://github.com/heroku/heroku-buildpack-python"
  ]

  source {
    path = "../application/bot"
  }
}

resource "heroku_build" "staging-frontend" {
  app_id = heroku_app.staging-frontend.id
  buildpacks = ["https://github.com/dokku/heroku-buildpack-nginx"]

  source {
    path = "../application/frontend/public"
  }

  depends_on = [
    data.external.frontend_build
  ]
}

resource "heroku_addon" "staging-papertrail-backend" {
  app_id = heroku_app.staging-backend.id
  plan = "papertrail:choklad"
}

resource "heroku_addon_attachment" "staging-papertrail-bot" {
  app_id  = heroku_app.staging-bot.id
  addon_id = heroku_addon.staging-papertrail-backend.id
}

# This creates the environment variable DATABASE_URL that we can use in our heroku_app
resource "heroku_addon" "staging-database" {
  app_id = heroku_app.staging-backend.id
  plan = "heroku-postgresql:hobby-dev"
}

# Needed to attach the database to a second app
resource "heroku_addon_attachment" "staging-database-attachment" {
  app_id  = heroku_app.staging-bot.id
  addon_id = heroku_addon.staging-database.id
}

resource "heroku_addon" "staging-batch-scheduler" {
  app_id = heroku_app.staging-bot.id
  plan = "scheduler:standard"
}

resource "herokux_scheduler_job" "staging-batch-scheduler-job" {
  app_id = heroku_app.staging-bot.id
  command = "python batch.py"
  dyno_size = "Free"
  frequency = "every_ten_minutes"

  # required in order for Terraform to wait for scheduler addon creation before creating jobs.
  depends_on = [heroku_addon.staging-batch-scheduler]
}

resource "heroku_formation" "staging-formation-backend" {
  app_id     = heroku_app.staging-backend.id
  type       = "web"
  quantity   = 1
  size       = "free"
  depends_on = [heroku_build.staging-backend]
}

resource "heroku_formation" "staging-formation-bot-worker" {
  app_id     = heroku_app.staging-bot.id
  type       = "batch"
  quantity   = 0
  size       = "free"
  depends_on = [heroku_build.staging-bot]
}

resource "heroku_formation" "staging-formation-bot-batch" {
  app_id     = heroku_app.staging-bot.id
  type       = "worker"
  quantity   = 1
  size       = "free"
  depends_on = [heroku_build.staging-bot]
}

resource "heroku_formation" "staging-formation-frontend" {
  app_id     = heroku_app.staging-frontend.id
  type       = "web"
  quantity   = 1
  size       = "free"
  depends_on = [heroku_build.staging-frontend]
}

resource "heroku_pipeline_coupling" "staging-backend" {
  app_id = heroku_app.staging-backend.id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "staging"
}

resource "heroku_pipeline_coupling" "staging-bot" {
  app_id = heroku_app.staging-bot.id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "staging"
}

resource "heroku_pipeline_coupling" "staging-frontend" {
  app_id = heroku_app.staging-frontend.id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "staging"
}