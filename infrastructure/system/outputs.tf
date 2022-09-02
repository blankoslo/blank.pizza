output "backend_app_url" {
  value       = heroku_app.backend.web_url
  description = "Backend application URL"
}

output "bot_app_url" {
  value       = heroku_app.bot.web_url
  description = "Backend application URL"
}

output "app_backend_id" {
    value       = heroku_app.backend.id
    description = "Backend app id"
}

output "app_bot_id" {
    value       = heroku_app.bot.id
    description = "Bot app id"
}

output "app_frontend_id" {
    value       = heroku_app.frontend.id
    description = "Frontend app id"
}