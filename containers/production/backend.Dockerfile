FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

ARG DB_USER
ARG DB_PASSWD
ARG DB_NAME
ARG DB_HOST
ARG DB_PORT
ENV DB_USER $DB_USER
ENV DB_PASSWD $DB_PASSWD
ENV DB_NAME $DB_NAME
ENV DB_HOST $DB_HOST
ENV DB_PORT $DB_PORT

COPY ./backend /app

WORKDIR /app

RUN \
 apk add --no-cache build-base && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r ./requirements.txt && \
 apk --purge del .build-deps