# pizza-app

## How to run the system

## Slack App Bot setup
1. Go to `https://api.slack.com/apps/`
2. Click the `Create New App` button
3. Choose `from scratch`
4. Give it a name and pick a workplace, and click create
5. Go to `App Home`
6. Go down to `Show Tabs` and switch on `Messages Tab` (to allow DMs)
7. Click `Socket mode` in the menu
8. Turn on `Connect using Socket Mode`
9. Click `Event Subscriptions`
10. Turn on `Enable Events`
11. Open `Subscribe to bot events`
12. Add the events `app_mention` `file_shared` `message.channels` `message.im`
~~13. Click `OAuth & Permissions` in the menu~~
~~14. Go down to `Scopes` and click `Add an OAuth Scope` and add the scopes `chat:write` `chat:write.customize` `chat:write.public` `im:write`~~
15. Go up to `OAuth Tokens for Your Workspace` and click `Install to Workspace`
16. Choose a channel and click `Allow`
17. Click `OAuth & Permissions` and copy the token at `Bot User OAuth Token` (this is the `SLACK_BOT_TOKEN`).
18. Click `Basic Information` in the menu
19. Go down to `App-Level Tokens` and click `Generate Token and Scopes`.
20. Write in a token name, click `Add scope` and choose both scopes.
21. Copy the Token (this is the `SLACK_APP_TOKEN`).
22. Now you have the `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` needed to run the bot.

## Development
The frontend, backend, bot (worker and batch), and database can all be run with docker compose by running `docker-compose up`. Optionally you can do `docker-compose up -d [service]` to only start one or more service. During development all services run behind an nginx instance to simplify their interactions. The ports are 80 and 443.

## Production
### Frontend
The frontend is a React application. Simply run the command `npm run build:production` and then host the files in your prefered cloud service for static files.

### Backend
The backend is a flask application. The easiest way to run it is to use the dockerfile in `/containers/production` in your prefered cloud service.

To build the image run the command `docker build --build-arg DB_NAME=pizza --build-arg DB_USER=postgres --build-arg DB_PASSWD=postgres --build-arg DB_HOST=host.docker.internal --build-arg DB_PORT=5432 -f backend.Dockerfile ../../` with the args `DB_USER` `DB_PASSWD` `DB_NAME` `DB_HOST` `DB_PORT` with your systems values.

To run the image run the command `docker run -e DB_NAME=pizza -e DB_USER=postgres -e DB_PASSWD=postgres -e DB_HOST=host.docker.internal -e DB_PORT=5432 -p 80:80 [id]` where `id` is the docker image id, with the args `DB_USER` `DB_PASSWD` `DB_NAME` `DB_HOST` `DB_PORT` with your systems values.

### Bot
The bot is a collection of python applications. The easiest way to run it is to use the dockerfiles starting with the name bot. in `/containers/production` in your prefered cloud service.

#### Worker
To build the image run the command `docker build --build-arg DB_HOST=host.docker.internal --build-arg DB_NAME=pizza --build-arg DB_USER=postgres --build-arg DB_PASSWD=postgres --build-arg SLACK_BOT_TOKEN=[bot-token] --build-arg SLACK_APP_TOKEN=[app-token] --build-arg PIZZA_CHANNEL_ID=[pizza-channel-id] -f bot.worker.Dockerfile ../../` with the args `DB_USER` `DB_PASSWD` `JDBC_URL` `SLACK_BOT_TOKEN` `SLACK_APP_TOKEN` `PIZZA_CHANNEL_ID` with your systems values.

To run the image run the command `docker run [id]` where `id` is the docker image id.

#### Batch
To build the image run the command `docker build --build-arg DB_HOST=host.docker.internal --build-arg DB_NAME=pizza --build-arg DB_USER=postgres --build-arg DB_PASSWD=postgres --build-arg SLACK_BOT_TOKEN=[bot-token] --build-arg SLACK_APP_TOKEN=[app-token] --build-arg PIZZA_CHANNEL_ID=[pizza-channel-id] -f bot.batch.Dockerfile ../../` with the args `DB_USER` `DB_PASSWD` `JDBC_URL` `SLACK_BOT_TOKEN` `SLACK_APP_TOKEN` `PIZZA_CHANNEL_ID` with your systems values.

To run the image run the command `docker run [id]` where `id` is the docker image id.