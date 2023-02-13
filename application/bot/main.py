#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import locale
import threading
import pytz
import logging
import sys

from src.api.bot_api import BotApiConfiguration

from src.scheduler import scheduler

from src.slack import slack_handler

from src.injector import injector, singleton
from src.broker.amqp_connection import AmqpConnection
from src.broker.amqp_connection_pool import AmqpConnectionPool
from src.broker.handlers import on_message

pizza_channel_id = os.environ["PIZZA_CHANNEL_ID"]

def setup_logger():
    logger = logging.getLogger(__name__)
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
    logger.addHandler(logging_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger

def setup_connection_pool():
    connection_pool = AmqpConnectionPool()
    injector.binder.bind(AmqpConnectionPool, to=connection_pool, scope=singleton)

def setup_consumption_queue_listener():
    mq = injector.get(AmqpConnection)
    mq.connect()
    mq.setup_exchange()
    mq.setup_queues()
    mq.setup_binding()
    def consume():
        mq.consume(on_message)
    consuming_thread = threading.Thread(target = consume)
    consuming_thread.start()

def main():
    # Set up injector
    api_config = BotApiConfiguration(pizza_channel_id, pytz.timezone('Europe/Oslo'))
    injector.binder.bind(BotApiConfiguration, to=api_config)

    # Set up logging
    logger = setup_logger()
    injector.binder.bind(logging.Logger, to=logger, scope=singleton)

    # Try setting locale
    try:
        locale.setlocale(locale.LC_ALL, "nb_NO.utf8")
    except:
        logger.warning("Missing locale nb_NO.utf8 on server")

    # Set up rabbitmq
    setup_connection_pool()
    setup_consumption_queue_listener()

    # start scheduler
    scheduler.start()

    # Start slack app
    slack_handler.start()

if __name__ == "__main__":
    main()
