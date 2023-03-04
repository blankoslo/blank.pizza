# pizza-app

## Slack App Bot setup
1. Go to `https://api.slack.com/apps/`
2. Click the `Create New App` button
3. Choose `from scratch`
4. Give it a name and pick a workplace, and click create
5. Click `Socket mode` in the menu
6. Turn on `Connect using Socket Mode`
7. Copy the Token (this is the `SLACK_APP_TOKEN`).
8. Click `Event Subscriptions`
9. Turn on `Enable Events`
10. Open `Subscribe to bot events`
11. Add the events `file_shared` `message.channels` `message.im`
12. Click `OAuth & Permissions` in the menu
13. Go down to `Scopes` and click `Add an OAuth Scope` and add the scopes `chat:write` `im:write` `users:read` `users:read.email`
14. Go to `App Home`
15. Go down to `Show Tabs` and switch on `Messages Tab` (to allow DMs)
16. Go to `OAuth & Permissions` under `Redirect URLs`
17. Add your install-redirect url which will be your domain (or localhost for development) + `/slack/callback`
18. Add your login-redirect url which will be your domain (or localhost for development) + `/login/callback`
19. Click `Basic Information` in the menu
20. `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `SLACK_SIGNING_SECRET`
21. You now have `SLACK_APP_TOKEN`, `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `SLACK_SIGNING_SECRET` which is needed in terraform or docker-compose

## How to run the system

### Development
The frontend, backend, bot (worker and batch), and database can all be run with docker compose by running `docker-compose up`. Optionally you can do `docker-compose up -d [service]` to only start one or more service. During development all services run behind an nginx instance to simplify their interactions. The ports are 80 and 443.

As we use Ouath2 for authentication we are forced to use https. Nginx needs valid ssl certificates, so you are gonna need to generate one with the command `openssl req -x509 -nodes -newkey rsa:4096 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt -sha256 -days 365` and add it to `application/containers/development`

### Good to know
Locales doesnt work properly in the alpine container used, meaning it's not a bug if stuff is localized wrong, such as the time string send in pizza event invites.

### Production
#### Terraform Cloud
This repository is connected to Terraform Cloud where it is automatically planned and then manually applied whenever a new tag is created.
The branch used in Terraform Cloud is the `Build` branch, which gets created on every new version. This branch is the same as master, but it also contains the build files for the frontend application.
A tag is automatically created through GitHub actions when a PR is merged into Main.

#### Heroku
We are using terraform to describe the infrastructure, which can be found in the `/infrastructure` folder. In addition to this the backend/bot have `Procfile`, `runtime.txt`, and `.locales` files that describe the process, heroku runtime and additional locales to include. While the frontend have `.static` in the `public` folder to indicate the application folder for the nginx buildpacker, and a `.gitignore` file to keep the files and folder in git.

1. Go into the `infrastructure` folder and run `terraform apply`.
    *  ~~optionally to only deploy staging run `terraform apply -target=module.staging -target=heroku_pipeline.pizzabot -target=heroku_pipeline_coupling.staging-backend -target=heroku_pipeline_coupling.staging-frontend -target=heroku_pipeline_coupling.staging-bot`~~
    *  ~~optionally to only deploy production run `terraform apply -target=module.production -target=heroku_pipeline.pizzabot -target=heroku_pipeline_coupling.production-backend -target=heroku_pipeline_coupling.production-frontend -target=heroku_pipeline_coupling.production-bot`~~
2. Add the urls from the heroku app (and or custom domain) to the Google OAuth client settings (the google ouath client should also be configured to be internal and be put into production (to not be limited to test users)).
3. Go to the app settings of the frontend app in Heroku at `https://dashboard.heroku.com/apps/pizzabot-v2-stag-frontend/settings` (where the text after `/apps/` will be your app's name) and under `Domains` copy the `DNS Target`.
4. Go to the app settings of the backend app in Heroku at `https://dashboard.heroku.com/apps/pizzabot-v2-stag-backend/settings` (where the text after `/apps/` will be your app's name) and under `Domains` copy the `DNS Target`.
5. Create a CNAME record with the hostname specified in the main terraform file for both the frontend and the backend and point them to the `DNS TARGET`s from heroku. After a while routing and SSL should work flawlesly.

Infrastructure:
* Backend-app: contains the database, papertrail instance, Rabbitmq instance, and backend application  
* Bot-app: contains an attachement to the database, an attachement to the papertrail instance, an attachement to the Rabbitmq instance, the bot worker
* Frontend-app: contains a nginx instance with the build files from the `public` folder
