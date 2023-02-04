variable "heroku_team_name" {
  type = string
}

variable "hostname" {
  type = string
}

variable "prefix" {
  type = string
}

variable "environment" {
  type = string
}

variable "MQ_EXCHANGE" {
  type = string
}

variable "MQ_EVENT_QUEUE" {
  type = string
}

variable "MQ_RPC_KEY" {
  type = string
}

variable "MQ_EVENT_KEY" {
  type = string
}

variable "PEOPLE_PER_EVENT" {
  type = number
}

variable "DAYS_IN_ADVANCE_TO_INVITE" {
  type = number
}

variable "REPLY_DEADLINE_IN_HOURS" {
  type = number
}

variable "HOURS_BETWEEN_REMINDERS" {
  type = number
}

variable "SLACK_BOT_TOKEN" {
  type = string
}

variable "SLACK_APP_TOKEN" {
  type = string
}

variable "PIZZA_CHANNEL_ID" {
  type = string
}

variable "SECRET_KEY_BACKEND" {
  type = string
}

variable "GOOGLE_CLIENT_ID" {
  type = string
}

variable "GOOGLE_CLIENT_SECRET" {
  type = string
}

variable "PAPERTRAIL_PLAN" {
  type = string
}

variable "CLOUDAMQP_PLAN" {
  type = string
}

variable "POSTGRES_PLAN" {
  type = string
}

variable "FLASK_ENV" {
  type = string
}

variable "FORMATION_SIZE_FRONTEND" {
  type = string
}

variable "FORMATION_SIZE_BACKEND" {
  type = string
}

variable "FORMATION_SIZE_BOT_WORKER" {
  type = string
}

variable "FORMATION_QUANTITY_FRONTEND" {
  type = string
}

variable "FORMATION_QUANTITY_BACKEND" {
  type = string
}

variable "FORMATION_QUANTITY_BOT_WORKER" {
  type = string
}

