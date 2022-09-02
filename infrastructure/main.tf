resource "heroku_pipeline" "pizzabot" {
  name = var.prefix
}

module "staging" {
  source = "./system"

  hostname = "staging.bot.blank.pizza"
  prefix = var.prefix
  environment = "stag"
  PAPERTRAIL_PLAN = "papertrail:choklad"
  POSTGRES_PLAN = "heroku-postgresql:hobby-dev"
  SCHEDULER_PLAN = "scheduler:standard"
  SCHEDULER_JOB_DYNO = "Free"
  SCHEDULER_JOB_FREQUENCY = "every_ten_minutes"
  FORMATION_SIZE_FRONTEND = "hobby"
  FORMATION_SIZE_BACKEND = "hobby"
  FORMATION_SIZE_BOT_WORKER = "hobby"
  FORMATION_SIZE_BOT_BATCH = "hobby"
  FORMATION_QUANTITY_FRONTEND = 1
  FORMATION_QUANTITY_BACKEND = 1
  FORMATION_QUANTITY_BOT_WORKER = 1
  FORMATION_QUANTITY_BOT_BATCH = 0
  SLACK_BOT_TOKEN = var.STAGING_SLACK_BOT_TOKEN
  SLACK_APP_TOKEN = var.STAGING_SLACK_APP_TOKEN
  PIZZA_CHANNEL_ID = var.STAGING_PIZZA_CHANNEL_ID
  SECRET_KEY_BACKEND = var.STAGING_SECRET_KEY_BACKEND
  GOOGLE_CLIENT_ID = var.STAGING_GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET = var.STAGING_GOOGLE_CLIENT_SECRET
}

module "production" {
  source = "./system"

hostname = "bot.blank.pizza"
  prefix = var.prefix
  environment = "prod"
  PAPERTRAIL_PLAN = "papertrail:choklad"
  POSTGRES_PLAN = "heroku-postgresql:hobby-dev"
  SCHEDULER_PLAN = "scheduler:standard"
  SCHEDULER_JOB_DYNO = "Free"
  SCHEDULER_JOB_FREQUENCY = "every_ten_minutes"
  FORMATION_SIZE_FRONTEND = "hobby"
  FORMATION_SIZE_BACKEND = "hobby"
  FORMATION_SIZE_BOT_WORKER = "hobby"
  FORMATION_SIZE_BOT_BATCH = "hobby"
  FORMATION_QUANTITY_FRONTEND = 1
  FORMATION_QUANTITY_BACKEND = 1
  FORMATION_QUANTITY_BOT_WORKER = 1
  FORMATION_QUANTITY_BOT_BATCH = 0
  SLACK_BOT_TOKEN = var.PRODUCTION_SLACK_BOT_TOKEN
  SLACK_APP_TOKEN = var.PRODUCTION_SLACK_APP_TOKEN
  PIZZA_CHANNEL_ID = var.PRODUCTION_PIZZA_CHANNEL_ID
  SECRET_KEY_BACKEND = var.PRODUCTION_SECRET_KEY_BACKEND
  GOOGLE_CLIENT_ID = var.PRODUCTION_GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET = var.PRODUCTION_GOOGLE_CLIENT_SECRET
}

# Add staging apps to pipeline under staging stage
resource "heroku_pipeline_coupling" "staging-backend" {
  app_id = module.staging.app_backend_id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "staging"
}

resource "heroku_pipeline_coupling" "staging-bot" {
  app_id = module.staging.app_bot_id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "staging"
}

resource "heroku_pipeline_coupling" "staging-frontend" {
  app_id = module.staging.app_frontend_id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "staging"
}

# Add production apps to pipeline under production stage
resource "heroku_pipeline_coupling" "production-backend" {
  app_id = module.production.app_backend_id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "production"
}

resource "heroku_pipeline_coupling" "production-bot" {
  app_id = module.production.app_bot_id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "production"
}

resource "heroku_pipeline_coupling" "production-frontend" {
  app_id = module.production.app_frontend_id
  pipeline = heroku_pipeline.pizzabot.id
  stage = "production"
}