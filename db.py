from psycopg2 import connect
import math
import os


def create_connection_string(db_host, db_name, db_user, db_passwd):
    return "host='{}' dbname='{}' user='{}' password='{}'".format(db_host, db_name, db_user, db_passwd)


def connect_to_pizza_db():
    db_host = os.environ["DB_HOST"]
    db_name = os.environ["DB_NAME"]
    db_user = os.environ["DB_USER"]
    db_passwd = os.environ["DB_PASSWD"]

    conn = connect(create_connection_string(
        db_host, db_name, db_user, db_passwd))
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
        AND invitations.rsvp = 'attending' AND invitations.event_id
        IN (SELECT id FROM events WHERE time < NOW() AND finalized = true ORDER BY time desc limit %s)
        WHERE NOT EXISTS (SELECT * FROM invitations WHERE invitations.event_id = %s
        AND invitations.slack_id = slack_users.slack_id)
        AND slack_users.active = TRUE
        GROUP BY slack_users.slack_id ORDER BY events_attended, random()
        LIMIT %s;
    """

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (number_of_events_regarded,
                               event_id, number_of_users_to_invite))
            rows = curs.fetchall()
            return [x[0] for x in rows]


def save_image(cloudinary_id, slack_id, title):
    sql = "INSERT INTO images (cloudinary_id, uploaded_by, title) VALUES (%s, %s, %s);"
    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (cloudinary_id, slack_id, title))


def save_invitations(slack_ids, event_id):
    values = [(event_id, slack_id) for slack_id in slack_ids]

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.executemany(
                "INSERT INTO invitations (event_id, slack_id) VALUES (%s, %s);", values)


def get_event_in_need_of_invitations(days_in_advance_to_invite, people_per_event):
    with pizza_conn:
        with pizza_conn.cursor() as curs:
            sql = """
                SELECT id, time, place, count(event_id) AS invited
                FROM events LEFT OUTER JOIN invitations on event_id = id
                AND (rsvp = 'unanswered' OR rsvp = 'attending')
                WHERE time > NOW() and time  < NOW() + interval '%s days'
                GROUP BY id
                HAVING count(event_id) < %s;
            """

            curs.execute(sql, (days_in_advance_to_invite, people_per_event))
            return curs.fetchone()


def get_invited_users():
    sql = "SELECT DISTINCT slack_id FROM invitations WHERE rsvp = 'unanswered';"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql)
            return [t[0] for t in curs.fetchall()]


def rsvp(slack_id, answer):
    sql = "UPDATE invitations SET rsvp = %s WHERE slack_id = %s AND rsvp = 'unanswered';"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (answer, slack_id))


def mark_event_as_finalized(event_id):
    sql = "UPDATE events SET finalized = true WHERE id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (event_id,))


def get_event_ready_to_finalize(people_per_event):
    sql = """
        SELECT event_id, time, place
        FROM slack_users, invitations, events
        WHERE  invitations.slack_id = slack_users.slack_id
        AND invitations.event_id = events.id
        AND rsvp = 'attending'
        AND not finalized
        GROUP BY event_id, time, place
        HAVING count(event_id) = %s;
    """

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (people_per_event,))
            return curs.fetchone()


def get_unanswered_invitations():
    sql = "SELECT slack_id, invited_at, reminded_at from invitations where rsvp = 'unanswered';"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql)
            return curs.fetchall()


def get_attending_users(event_id):
    sql = "SELECT slack_id FROM invitations WHERE rsvp = 'attending' and event_id = %s ORDER BY random();"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (event_id,))
            return [t[0] for t in curs.fetchall()]


def get_slack_ids_from_emails(emails):
    sql = "select slack_id from slack_users where email in ('%s');" % (
        "','".join(emails))

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql)
            return [t[0] for t in curs.fetchall()]


def update_reminded_at(slack_id):
    sql = "UPDATE invitations SET reminded_at = 'NOW()' where rsvp = 'unanswered' and slack_id = %s;"

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (slack_id,))


def auto_reply_after_deadline(deadline):
    sql = """
        UPDATE invitations
        SET rsvp = 'not attending'
        WHERE rsvp = 'unanswered'
        AND invited_at < NOW() - interval '%s hours' returning slack_id;
    """

    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql, (deadline,))


def get_previous_pizza_events():
    events = """
        SELECT time, place, string_agg(current_username,', ') AS attendees, events.id FROM events
        INNER JOIN invitations ON events.id = invitations.event_id
        INNER JOIN slack_users ON invitations.slack_id = slack_users.slack_id
        WHERE events.finalized = TRUE AND invitations.rsvp = 'attending'
        GROUP BY events.id;
    """
    with pizza_conn:
        with pizza_conn.cursor() as curs:
            curs.execute(sql)
            return curs.fetchall()

    
