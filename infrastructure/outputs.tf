output "backend_app_url" {
  value       = heroku_app.staging-backend.web_url
  description = "Backend application URL"
}

output "bot_app_url" {
  value       = heroku_app.staging-bot.web_url
  description = "Backend application URL"
}