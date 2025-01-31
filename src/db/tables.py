from .postgres import create_connection


def create_table(table_name, columns):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE TABLE {table_name} ({columns})")
            connection.commit()


def rename_table(table_name, new_table_name):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER TABLE {table_name} RENAME TO {new_table_name}")
            connection.commit()


def delete_table(table_name):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE {table_name}")
            connection.commit()


def is_table_empty(table_name):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0] == 0
