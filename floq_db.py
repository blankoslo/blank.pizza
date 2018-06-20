from psycopg2 import connect
import math
import os


def create_connection_string(db_host, db_name, db_user, db_passwd):
    return "host='{}' dbname='{}' user='{}' password='{}'".format(db_host, db_name, db_user, db_passwd)


def connect_to_floq_db():
    db_host = os.environ["FLOQ_DB_HOST"]
    db_name = os.environ["FLOQ_DB_NAME"]
    db_user = os.environ["FLOQ_DB_USER"]
    db_passwd = os.environ["FLOQ_DB_PASSWD"]

    conn = connect(create_connection_string(
        db_host, db_name, db_user, db_passwd))
    return conn


floq_conn = connect_to_floq_db()


def get_users_with_first_day():
    sql = "select email from employees where date_of_employment = current_date;"

    with floq_conn:
        with floq_conn.cursor() as curs:
            curs.execute(sql)
            return [t[0] for t in curs.fetchall()]


def get_users_with_birthday():
    sql = "select email from employees where extract(month from birth_date) = extract(month from current_date) and extract(day from birth_date) = extract(day from current_date) and (termination_date is null OR termination_date >= current_date);"

    with floq_conn:
        with floq_conn.cursor() as curs:
            curs.execute(sql)
            return [t[0] for t in curs.fetchall()]
