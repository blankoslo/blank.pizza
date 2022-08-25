FROM python:3.6-alpine

ARG DB_USER
ARG DB_PASSWD
ARG DB_NAME
ARG DB_HOST
ARG SLACK_BOT_TOKEN
ARG SLACK_APP_TOKEN
ARG PIZZA_CHANNEL_ID
ENV DB_USER $DB_USER
ENV DB_PASSWD $DB_PASSWD
ENV DB_NAME $DB_NAME
ENV DB_HOST $DB_HOST
ENV SLACK_BOT_TOKEN $SLACK_BOT_TOKEN
ENV SLACK_APP_TOKEN $SLACK_APP_TOKEN
ENV PIZZA_CHANNEL_ID $PIZZA_CHANNEL_ID

COPY /bot/ /app
WORKDIR /app

RUN \
 apk add --no-cache build-base && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt && \
 apk --purge del .build-deps

EXPOSE 80
EXPOSE 443
EXPOSE 5432

CMD python batch.py