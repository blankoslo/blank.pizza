variable "prefix" {
  description = "High-level name of this configuration, used as a resource name prefix"
  type = string
  default = "pizzabot-v2"
}

variable "heroku_api_key" {
  type = string
}

variable "heroku_api_email" {
  type = string
}

variable "heroku_team_id" {
  type = string
}

variable "heroku_team_name" {
  type = string
}

# ************* STAGING ************* #
variable "STAGING_SLACK_BOT_TOKEN" {
  type = string
}

variable "STAGING_SLACK_APP_TOKEN" {
  type = string
}

variable "STAGING_PIZZA_CHANNEL_ID" {
  type = string
}

variable "STAGING_SECRET_KEY_BACKEND" {
  type = string
}

variable "STAGING_GOOGLE_CLIENT_ID" {
  type = string
}

variable "STAGING_GOOGLE_CLIENT_SECRET" {
  type = string
}

# ************* PRODUCTION ************* #
variable "PRODUCTION_SLACK_BOT_TOKEN" {
  type = string
}

variable "PRODUCTION_SLACK_APP_TOKEN" {
  type = string
}

variable "PRODUCTION_PIZZA_CHANNEL_ID" {
  type = string
}

variable "PRODUCTION_SECRET_KEY_BACKEND" {
  type = string
}

variable "PRODUCTION_GOOGLE_CLIENT_ID" {
  type = string
}

variable "PRODUCTION_GOOGLE_CLIENT_SECRET" {
  type = string
}