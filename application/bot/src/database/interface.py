from psycopg2 import connect, extensions
import math
import os
from urllib.parse import urlparse
from psycopg2.extensions import register_adapter, AsIs

from src.database.rsvp import RSVP

def adapt_RSVP_type(rsvp_type: RSVP):
    return AsIs(f"'{rsvp_type.value}'")

register_adapter(RSVP, adapt_RSVP_type)

def cast_RSVP_type(value, cur):
    if value is None:
        return None
    return RSVP(value)

type_cast_RSVP_type = extensions.new_type((17066, ), "RSVP", cast_RSVP_type)
extensions.register_type(type_cast_RSVP_type)

def create_connection_string(db_host, db_name, db_user, db_passwd, db_port):
    return f"host='{db_host}' dbname='{db_name}' user='{db_user}' password='{db_passwd}' port='{db_port}'"

def create_connection_string_from_uri(uri):
    result = urlparse(uri)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    return create_connection_string(db_host=hostname, db_name=database, db_user=username, db_passwd=password, db_port=port)

def connect_to_pizza_db():
    if ("DATABASE_URL" in os.environ):
        db_uri = os.environ["DATABASE_URL"]
        connection_string = create_connection_string_from_uri(db_uri)
        conn = connect(connection_string)
    else:
        db_host = os.environ["DB_HOST"]
        db_name = os.environ["DB_NAME"]
        db_user = os.environ["DB_USER"]
        db_passwd = os.environ["DB_PASSWD"]
        db_port = os.environ["DB_PORT"]
        connection_string = create_connection_string(db_host, db_name, db_user, db_passwd, db_port)
        conn = connect(connection_string)
    
    return conn


pizza_conn = connect_to_pizza_db()

def event_in_past(event_id):
    sql = """
        SELECT CAST(CASE WHEN time < NOW() THEN 'true' ELSE 'false' END AS boolean)
        FROM events
        WHERE id = %s
    """

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (event_id,))
            res = curs.fetchone()
            return res[0]

def update_invitation(event_id, slack_id, rsvp):
    # TODO, add option to only allow update if event is after NOW
    sql = "UPDATE invitations SET rsvp = %s WHERE slack_id = %s AND event_id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (rsvp, slack_id, event_id,))

def event_is_finalized(event_id):
    sql = "SELECT finalized from events WHERE id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (event_id,))
            finalized = curs.fetchone()
            return finalized[0]

def mark_event_as_unfinalized(event_id):
    sql = "UPDATE events SET finalized = false WHERE id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (event_id,))

