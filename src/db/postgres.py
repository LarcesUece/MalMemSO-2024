from psycopg2 import connect, Error
from flask import current_app as app


def create_connection():
    user = app.config.get("POSTGRES_USER")
    password = app.config.get("POSTGRES_PASSWORD")
    database = app.config.get("POSTGRES_DB")
    host = app.config.get("POSTGRES_HOST")
    port = app.config.get("POSTGRES_PORT")

    if (
        user is None
        or password is None
        or database is None
        or host is None
        or port is None
    ):
        raise ValueError("Missing database configuration.")

    try:
        connection = connect(
            user=user, password=password, database=database, host=host, port=port
        )
        app.logger.info("Connected to the database.")
    except Error:
        raise Error("Failed to connect to the database.")

    return connection
