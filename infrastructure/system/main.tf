resource "heroku_domain" "blank" {
  app_id   = heroku_app.frontend.id
  hostname = var.hostname
}

resource "heroku_app" "backend" {
  name = "${var.prefix}-${var.environment}-backend"
  region = "eu"
  stack = "heroku-22"

  organization {
    name = var.heroku_team_name
  }

  config_vars = {
    "MQ_EXCHANGE" = var.MQ_EXCHANGE
    "MQ_EVENT_QUEUE" = var.MQ_EVENT_QUEUE
    "MQ_RPC_KEY" = var.MQ_RPC_KEY
    "MQ_EVENT_KEY" =  var.MQ_EVENT_KEY
    "PEOPLE_PER_EVENT" = var.PEOPLE_PER_EVENT
    "DAYS_IN_ADVANCE_TO_INVITE" = var.DAYS_IN_ADVANCE_TO_INVITE
    "FLASK_ENV" = var.FLASK_ENV
  }

  sensitive_config_vars = {
    "SECRET_KEY" = var.SECRET_KEY_BACKEND
    "GOOGLE_CLIENT_ID" = var.GOOGLE_CLIENT_ID
    "GOOGLE_CLIENT_SECRET" = var.GOOGLE_CLIENT_SECRET
  }
}

resource "heroku_app" "bot" {
  name = "${var.prefix}-${var.environment}-bot"
  region = "eu"
  stack = "heroku-22"

  organization {
    name = var.heroku_team_name
  }

  config_vars = {
    "MQ_EXCHANGE" = var.MQ_EXCHANGE
    "MQ_EVENT_QUEUE" = var.MQ_EVENT_QUEUE
    "MQ_RPC_KEY" = var.MQ_RPC_KEY
    "MQ_EVENT_KEY" =  var.MQ_EVENT_KEY
    "REPLY_DEADLINE_IN_HOURS" = var.REPLY_DEADLINE_IN_HOURS
    "HOURS_BETWEEN_REMINDERS" = var.HOURS_BETWEEN_REMINDERS
  }

  sensitive_config_vars = {
    "SLACK_BOT_TOKEN" = var.SLACK_BOT_TOKEN
    "SLACK_APP_TOKEN" = var.SLACK_APP_TOKEN
    "PIZZA_CHANNEL_ID" = var.PIZZA_CHANNEL_ID
  }
}

# NB: FRONTEND_URI must be set to the ssl custom domain "https://${var.hostname}" for the OAuth to work
resource "heroku_config" "endpoints" {
    vars = {
        FRONTEND_URI = var.FRONTEND_URI
        BACKEND_URI = var.BACKEND_URI
    }
}

resource "heroku_app_config_association" "config_backend_association" {
  app_id = heroku_app.backend.id

  vars = heroku_config.endpoints.vars
  sensitive_vars = heroku_config.endpoints.sensitive_vars
}

resource "heroku_app" "frontend" {
  name = "${var.prefix}-${var.environment}-frontend"
  region = "eu"
  stack = "heroku-22"

  acm = true

  organization {
    name = var.heroku_team_name
  }

  config_vars = {
    "NGINX_DEFAULT_REQUEST" = "index.html"
  }
}

resource "heroku_build" "backend" {
  app_id = heroku_app.backend.id
  buildpacks = [
    "https://github.com/heroku/heroku-buildpack-locale",
    "https://github.com/heroku/heroku-buildpack-python"
  ]

  source {
    path = "../application/backend"
  }
}

resource "heroku_build" "bot" {
  app_id = heroku_app.bot.id
  buildpacks = [
    "https://github.com/heroku/heroku-buildpack-locale",
    "https://github.com/heroku/heroku-buildpack-python"
  ]

  source {
    path = "../application/bot"
  }
}

resource "heroku_build" "frontend" {
  app_id = heroku_app.frontend.id
  buildpacks = ["https://github.com/dokku/heroku-buildpack-nginx"]

  source {
    path = "../application/frontend/public"
  }
}

resource "heroku_addon" "cloudamqp-backend" {
  name = "${var.prefix}-${var.environment}-cloudamqp"
  app_id = heroku_app.backend.id
  plan = var.CLOUDAMQP_PLAN
}

resource "heroku_addon_attachment" "cloudamqp-bot" {
  app_id  = heroku_app.bot.id
  addon_id = heroku_addon.cloudamqp-backend.id
}

resource "heroku_addon" "papertrail-backend" {
  name = "${var.prefix}-${var.environment}-papertrail"
  app_id = heroku_app.backend.id
  plan = var.PAPERTRAIL_PLAN
}

resource "heroku_addon_attachment" "papertrail-bot" {
  app_id  = heroku_app.bot.id
  addon_id = heroku_addon.papertrail-backend.id
}

# This creates the environment variable DATABASE_URL that we can use in our heroku_app
resource "heroku_addon" "database" {
  name = "${var.prefix}-${var.environment}-database"
  app_id = heroku_app.backend.id
  plan = var.POSTGRES_PLAN
}

# Needed to attach the database to a second app
resource "heroku_addon_attachment" "database-attachment" {
  app_id  = heroku_app.bot.id
  addon_id = heroku_addon.database.id
}

#resource "herokux_postgres_backup_schedule" "database_backup" {
#  postgres_id = heroku_addon.database.id
#  hour        = 23
#  timezone    = "Europe/Oslo"
#}

resource "heroku_formation" "formation-backend" {
  app_id     = heroku_app.backend.id
  type       = "web"
  quantity   = var.FORMATION_QUANTITY_BACKEND
  size       = var.FORMATION_SIZE_BACKEND
  depends_on = [heroku_build.backend]
}

resource "heroku_formation" "formation-bot-worker" {
  app_id     = heroku_app.bot.id
  type       = "worker"
  quantity   = var.FORMATION_QUANTITY_BOT_WORKER
  size       = var.FORMATION_SIZE_BOT_WORKER
  depends_on = [heroku_build.bot]
}

resource "heroku_formation" "formation-frontend" {
  app_id     = heroku_app.frontend.id
  type       = "web"
  quantity   = var.FORMATION_QUANTITY_FRONTEND
  size       = var.FORMATION_SIZE_FRONTEND
  depends_on = [heroku_build.frontend]
}
