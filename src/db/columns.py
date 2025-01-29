from .postgres import create_connection


def add_column_to_table(table_name, column_name, column_type):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            )
            connection.commit()


def rename_column_in_table(table_name, column_name, new_column_name):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {new_column_name}"
            )
            connection.commit()
