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


def update_slack_users(slack_users):
    usernames = [(u['id'], u['name'], u['profile']['email'])
                 for u in slack_users]

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.executemany(
                "INSERT INTO slack_users (slack_id, current_username, email) VALUES (%s,%s,%s) ON CONFLICT (slack_id) DO UPDATE SET current_username = EXCLUDED.current_username, email = EXCLUDED.email;", usernames)


def get_users_to_invite(number_of_users_to_invite, event_id, total_number_of_employees, employees_per_event):
    number_of_events_regarded = math.ceil(
        total_number_of_employees / employees_per_event)

    sql = """
        SELECT slack_users.slack_id, count(rsvp) AS events_attended
        FROM slack_users
        LEFT JOIN invitations ON slack_users.slack_id = invitations.slack_id
        AND invitations.rsvp = %s AND invitations.event_id
        IN (SELECT id FROM events WHERE time < NOW() AND finalized = true ORDER BY time desc limit %s)
        WHERE NOT EXISTS (SELECT * FROM invitations WHERE invitations.event_id = %s
        AND invitations.slack_id = slack_users.slack_id)
        AND slack_users.active = TRUE
        GROUP BY slack_users.slack_id ORDER BY events_attended, random()
        LIMIT %s;
    """

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (RSVP.attending, number_of_events_regarded,
                               event_id, number_of_users_to_invite,))
            rows = curs.fetchall()
            return [x[0] for x in rows]


def save_image(cloudinary_id, slack_id, title):
    sql = "INSERT INTO images (cloudinary_id, uploaded_by_id, title) VALUES (%s, %s, %s);"
    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (cloudinary_id, slack_id, title,))


def save_invitations(slack_ids, event_id):
    values = [(event_id, slack_id) for slack_id in slack_ids]

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.executemany(
                "INSERT INTO invitations (event_id, slack_id) VALUES (%s, %s);", values)


def get_events_in_need_of_invitations(days_in_advance_to_invite, people_per_event):
    with pizza_conn:
        with pizza_conn.cursor() as curs:
            # TODO This query might need to be tested
            sql = """
                select events.id, events.time, events.restaurant_id, count(invitations.event_id) AS invited, restaurants.name
                FROM events
                left outer join restaurants on events.restaurant_id = restaurants.id
                LEFT OUTER JOIN invitations on invitations.event_id = events.id
                AND (invitations.rsvp = %s OR invitations.rsvp = %s)
                WHERE events.time > NOW() and events.time  < NOW() + interval '%s days'
                GROUP BY events.id, restaurants.name
                HAVING count(invitations.event_id) < %s;
            """

            curs.execute(sql, (RSVP.unanswered, RSVP.attending, days_in_advance_to_invite, people_per_event,))
            return curs.fetchall()

def get_event_in_need_of_invitations(days_in_advance_to_invite, people_per_event):
    events = get_events_in_need_of_invitations(days_in_advance_to_invite, people_per_event)
    return events[0]

def get_invited_users():
    sql = "SELECT DISTINCT slack_id FROM invitations WHERE rsvp = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (RSVP.unanswered,))
            return [t[0] for t in curs.fetchall()]


def rsvp(slack_id, answer):
    sql = "UPDATE invitations SET rsvp = %s WHERE slack_id = %s AND rsvp = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (answer, slack_id, RSVP.unanswered,))

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

def mark_event_as_finalized(event_id):
    sql = "UPDATE events SET finalized = true WHERE id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (event_id,))


def get_event_ready_to_finalize(people_per_event):
    sql = """
        SELECT event_id, time, restaurant_id
        FROM slack_users, invitations, events
        WHERE  invitations.slack_id = slack_users.slack_id
        AND invitations.event_id = events.id
        AND rsvp = %s
        AND not finalized
        GROUP BY event_id, time, restaurant_id
        HAVING count(event_id) = %s;
    """

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (RSVP.attending, people_per_event,))
            return curs.fetchone()


def get_unanswered_invitations():
    sql = "SELECT slack_id, invited_at, reminded_at from invitations where rsvp = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (RSVP.unanswered,))
            return curs.fetchall()


def get_attending_users(event_id):
    sql = "SELECT slack_id FROM invitations WHERE rsvp = %s and event_id = %s ORDER BY random();"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (RSVP.attending, event_id,))
            return [t[0] for t in curs.fetchall()]


def get_slack_ids_from_emails(emails):
    sql = "select slack_id from slack_users where email in ('%s');" % (
        "','".join(emails))

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql)
            return [t[0] for t in curs.fetchall()]


def update_reminded_at(slack_id):
    sql = "UPDATE invitations SET reminded_at = 'NOW()' where rsvp = %s and slack_id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (RSVP.unanswered, slack_id,))


def auto_reply_after_deadline(deadline):
    sql = """
        UPDATE invitations
        SET rsvp = %s
        WHERE rsvp = %s
        AND invited_at < NOW() - interval '%s hours' returning slack_id;
    """

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (RSVP.not_attending, RSVP.unanswered, deadline,))

def get_restaurant(id):
    sql = "SELECT * from restaurants where id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (id,))
            return curs.fetchone()

def get_restaurant_name(id):
    id, name, link, tlf, address, deleted = get_restaurant(id)
    return name