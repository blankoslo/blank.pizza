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
11. Add the events `app_mention` `file_shared` `message.channels` `message.im`
12. Click `OAuth & Permissions` in the menu
13. Go down to `Scopes` and click `Add an OAuth Scope` and add the scopes `chat:write` `im:write` `users:read` `users:read.email`
14. Go to `App Home`
15. Go down to `Show Tabs` and switch on `Messages Tab` (to allow DMs)
16. Go up to `OAuth Tokens for Your Workspace` and click `Install to Workspace`
17. Choose a channel and click `Allow`
18. Click `OAuth & Permissions` and copy the token at `Bot User OAuth Token` (this is the `SLACK_BOT_TOKEN`).
19. Click `Basic Information` in the menu
20. Now you have the `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` needed to run the bot.

## Google Login Setup
1. Go to the [Google developers credentials page](https://console.developers.google.com/apis/credentials)
2. If you don't have a project, create one, else choose the prefered project.
2. Press the Create credentials button
3. Select the option for `OAuth client ID`
4. Click `Configure consent screen`
    1. If open for all users choose `External`, but if only open for an organization like `blank.no` then choose `Internal`.
    2. Fill out the necessary information for the conest screen
    3. Click `Add or remove scopes` and add `.../auth/userinfo.email`	`.../auth/userinfo.profile` `openid`.
    4. If you are testing add a test user for testing
5. Choose `Web application`
6. Give it a name 
6. Set the Authorized JavaScript origins 
    * If testing then set to `https://localhost` and Authorized redirect URIs to `https://localhost/api/auth/login/callback`
    * If production then replace `localhost` with your domain
7. Hit Create and take note of the `client ID` and `client secret`

## How to run the system

### Development
The frontend, backend, bot (worker and batch), and database can all be run with docker compose by running `docker-compose up`. Optionally you can do `docker-compose up -d [service]` to only start one or more service. During development all services run behind an nginx instance to simplify their interactions. The ports are 80 and 443.

As we use Ouath2 for authentication we are forced to use https. Nginx needs valid ssl certificates, so you are gonna need to generate one with the command `openssl req -x509 -nodes -newkey rsa:4096 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt -sha256 -days 365` and add it to `application/containers/development`

### Production
#### Heroku
We are using terraform to describe the infrastructure, which can be found in the `/infrastructure` folder. In addition to this the backend/bot have `Procfile` and `runtime.txt` files that describe the process and heroku runtime. While the frontend have `.static` in the `public` folder to indicate the application folder for the nginx buildpacker, and a `.gitignore` file to keep the files and folder in git.

1. Go into the `infrastructure` folder and run `terraform apply`.
2. Add the urls from the heroku app to the Google OAuth client settings (the google ouath client should also be configured to be internal and be put into production (to not be limited to test users)).

Infrastructure:  
* Backend-app: contains the database, papertrail instance, and backend application  
* Bot-app: contains an attachement to the database,, an attachement to the papertrail instance, the bot worker, the bot batch (not running), scheduler and scheduler job  
* Frontend-app: contains an nginx instance with the build files from the `public` folder  

#### Cloud / Docker
It should be fairly straight forward to deploy to other cloud services by using the production docker containers in `application/containers/production`. However, Heroku and Terraform didnt fully support using docker (as the build context would be the same location as the Dockerfile which would ruin the folder structure. The fact that everything application related is put into the `application` folder is already from a limition in terraform/heroku), as such docker won't be used for this project as of now, but they are here for when they are needed.

##### Frontend
The frontend is a React application. Simply run the command `npm run build:production` and then host the files in your prefered cloud service for static files.

##### Backend
The backend is a flask application. The easiest way to run it is to use the dockerfile in `/containers/production` in your prefered cloud service.

To build the image run the command `docker build --build-arg DB_NAME=pizza --build-arg DB_USER=postgres --build-arg DB_PASSWD=postgres --build-arg DB_HOST=host.docker.internal --build-arg DB_PORT=5432 --build-arg FRONTEND_URI=[frontend_uri] -f backend.Dockerfile ../../` with the args `DB_USER` `DB_PASSWD` `DB_NAME` `DB_HOST` `DB_PORT` `FRONTEND_URI` with your systems values.

To run the image run the command `docker run -e DB_NAME=pizza -e DB_USER=postgres -e DB_PASSWD=postgres -e DB_HOST=host.docker.internal -e DB_PORT=5432 -e FRONTEND_URI=[frontend_uri] -p 80:80 [id]` where `id` is the docker image id, with the args `DB_USER` `DB_PASSWD` `DB_NAME` `DB_HOST` `DB_PORT` `FRONTEND_URI` with your systems values.

##### Bot
The bot is a collection of python applications. The easiest way to run it is to use the dockerfiles starting with the name bot. in `/containers/production` in your prefered cloud service.

###### Worker
To build the image run the command `docker build --build-arg DB_HOST=host.docker.internal --build-arg DB_NAME=pizza --build-arg DB_USER=postgres --build-arg DB_PASSWD=postgres --build-arg SLACK_BOT_TOKEN=[bot-token] --build-arg SLACK_APP_TOKEN=[app-token] --build-arg PIZZA_CHANNEL_ID=[pizza-channel-id] -f bot.worker.Dockerfile ../../` with the args `DB_USER` `DB_PASSWD` `JDBC_URL` `SLACK_BOT_TOKEN` `SLACK_APP_TOKEN` `PIZZA_CHANNEL_ID` with your systems values.

To run the image run the command `docker run [id]` where `id` is the docker image id.

###### Batch
To build the image run the command `docker build --build-arg DB_HOST=host.docker.internal --build-arg DB_NAME=pizza --build-arg DB_USER=postgres --build-arg DB_PASSWD=postgres --build-arg SLACK_BOT_TOKEN=[bot-token] --build-arg SLACK_APP_TOKEN=[app-token] --build-arg PIZZA_CHANNEL_ID=[pizza-channel-id] -f bot.batch.Dockerfile ../../` with the args `DB_USER` `DB_PASSWD` `JDBC_URL` `SLACK_BOT_TOKEN` `SLACK_APP_TOKEN` `PIZZA_CHANNEL_ID` with your systems values.

To run the image run the command `docker run [id]` where `id` is the docker image id.
