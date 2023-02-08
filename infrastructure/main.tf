resource "heroku_pipeline" "pizzabot" {
  name = var.prefix

  owner {
    id = var.heroku_team_id
    type = "team"
  }
}

module "staging" {
  source = "./system"

  heroku_team_name = var.heroku_team_name
  hostname = "staging.bot.blank.pizza"
  prefix = var.prefix
  environment = "stag"
  CLOUDAMQP_PLAN = "cloudamqp:lemur"
  PAPERTRAIL_PLAN = "papertrail:choklad"
  POSTGRES_PLAN = "heroku-postgresql:mini"
  FORMATION_SIZE_FRONTEND = "Basic"
  FORMATION_SIZE_BACKEND = "Basic"
  FORMATION_SIZE_BOT_WORKER = "Basic"
  FORMATION_QUANTITY_FRONTEND = 1
  FORMATION_QUANTITY_BACKEND = 1
  FORMATION_QUANTITY_BOT_WORKER = 1
  SLACK_BOT_TOKEN = var.STAGING_SLACK_BOT_TOKEN
  SLACK_APP_TOKEN = var.STAGING_SLACK_APP_TOKEN
  PIZZA_CHANNEL_ID = var.STAGING_PIZZA_CHANNEL_ID
  SECRET_KEY_BACKEND = var.STAGING_SECRET_KEY_BACKEND
  GOOGLE_CLIENT_ID = var.STAGING_GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET = var.STAGING_GOOGLE_CLIENT_SECRET
  MQ_EVENT_KEY = "pizza"
  MQ_EVENT_QUEUE = "Pizza_Queue"
  MQ_EXCHANGE = "Pizza_Exchange"
  MQ_RPC_KEY = "rpc"
  PEOPLE_PER_EVENT = 5
  DAYS_IN_ADVANCE_TO_INVITE = 10
  HOURS_BETWEEN_REMINDERS = 4
  REPLY_DEADLINE_IN_HOURS = 24
  FLASK_ENV = "production"
}

/*
module "production" {
  source = "./system"

  heroku_team_name = var.heroku_team_name
  hostname = "bot.blank.pizza"
  prefix = var.prefix
  environment = "prod"
  CLOUDAMQP_PLAN = "cloudamqp:lemur"
  PAPERTRAIL_PLAN = "papertrail:choklad"
  POSTGRES_PLAN = "heroku-postgresql:mini"
  FORMATION_SIZE_FRONTEND = "Basic"
  FORMATION_SIZE_BACKEND = "Basic"
  FORMATION_SIZE_BOT_WORKER = "Basic"
  FORMATION_QUANTITY_FRONTEND = 1
  FORMATION_QUANTITY_BACKEND = 1
  FORMATION_QUANTITY_BOT_WORKER = 1
  SLACK_BOT_TOKEN = var.PRODUCTION_SLACK_BOT_TOKEN
  SLACK_APP_TOKEN = var.PRODUCTION_SLACK_APP_TOKEN
  PIZZA_CHANNEL_ID = var.PRODUCTION_PIZZA_CHANNEL_ID
  SECRET_KEY_BACKEND = var.PRODUCTION_SECRET_KEY_BACKEND
  GOOGLE_CLIENT_ID = var.PRODUCTION_GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET = var.PRODUCTION_GOOGLE_CLIENT_SECRET
  MQ_EVENT_KEY = "pizza"
  MQ_EVENT_QUEUE = "Pizza_Queue"
  MQ_EXCHANGE = "Pizza_Exchange"
  MQ_RPC_KEY = "rpc"
  PEOPLE_PER_EVENT = 5
  DAYS_IN_ADVANCE_TO_INVITE = 10
  HOURS_BETWEEN_REMINDERS = 4
  REPLY_DEADLINE_IN_HOURS = 24
  FLASK_ENV = "production"
}*/

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

/*
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
*/
