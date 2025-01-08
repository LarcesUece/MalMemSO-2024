import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import warnings

import config
import utils


def connect() -> psycopg2.extensions.connection:
    """Connect to the PostgreSQL database server and return the connection object."""

    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS,
        )
        print("Connected to database.")
        return conn
    except Exception:
        print("Error connecting to database.")
        raise


def create_table(
    table_name: str, df: pd.DataFrame = None, columns: list[tuple] = None
) -> None:
    """Create a table in the PostgreSQL database."""

    conn = connect()
    cur = conn.cursor()

    if table_exists(table_name):
        print(f"Table '{table_name}' already exists.")
        return

    if df is not None:
        query = utils.generate_create_table_query(table_name, df=df)
    elif columns is not None:
        query = utils.generate_create_table_query(table_name, columns=columns)
    else:
        print("No data or columns provided.")
        raise ValueError

    print(query)

    try:
        cur.execute(query)
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except Exception:
        conn.rollback()
        print(f"Error creating table '{table_name}'.")
        raise
    finally:
        cur.close()
        conn.close()


def insert_data_to_postgres(
    table_name: str, df: pd.DataFrame = None, data: dict | list[dict] = None
) -> None:
    """Insert a pandas DataFrame or a dict into a PostgreSQL table."""

    if df is None and data is None:
        print("No data provided.")
        raise ValueError

    conn = connect()
    cur = conn.cursor()

    if df is not None:
        values = [tuple(x) for x in df.to_numpy()]
        cols = ",".join(f'"{col}"' for col in df.columns)
        query = f"INSERT INTO {table_name} ({cols}) VALUES %s"

    elif data is not None:
        cols = data.keys()
        placeholders = ", ".join([f"%({col})s" for col in cols])
        query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({placeholders})"

    try:
        if df is not None:
            execute_values(cur, query, values)
        elif data is not None:
            cur.execute(query, data)

        conn.commit()
        print(f"Data inserted into '{table_name}' successfully.")
    except Exception:
        conn.rollback()
        print(f"Error inserting data into '{table_name}'.")
        raise
    finally:
        cur.close()
        conn.close()


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the PostgreSQL database."""

    conn = connect()
    cur = conn.cursor()

    query = """
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = %s
    );"""

    try:
        cur.execute(query, (table_name,))
        exists = cur.fetchone()[0]
        return exists
    except Exception:
        print("Error checking if table exists.")
        return False
    finally:
        cur.close()
        conn.close()


def table_has_data(table_name: str) -> bool:
    """Check if a table has data in the PostgreSQL database."""

    conn = connect()
    cur = conn.cursor()

    query = f"SELECT COUNT(*) FROM {table_name};"

    try:
        cur.execute(query)
        count = cur.fetchone()[0]
        return count > 0
    except psycopg2.errors.UndefinedTable:
        return False
    except Exception:
        print(f"Error checking if table '{table_name}' has data.")
        return False
    finally:
        cur.close()
        conn.close()


def insert_initial_data():
    """Insert initial data into the database if the table is empty or does not exist."""

    if not table_exists(config.DATA_TABLE):
        df = pd.read_csv(config.INITIAL_DATA_FILE)
        create_table(config.DATA_TABLE, df)
        insert_data_to_postgres(config.DATA_TABLE, df=df)
        print("Initial data inserted.")
    elif not table_has_data(config.DATA_TABLE):
        df = pd.read_csv(config.INITIAL_DATA_FILE)
        insert_data_to_postgres(config.DATA_TABLE, df=df)
        print("Initial data inserted.")


def delete_data_from_table(table_name: str) -> None:
    """Delete all data from a table in the PostgreSQL database."""

    conn = connect()
    cur = conn.cursor()

    query = f"DELETE FROM {table_name};"

    try:
        cur.execute(query)
        conn.commit()
        print(f"Data deleted from '{table_name}' successfully.")
    except Exception:
        conn.rollback()
        print(f"Error deleting data from '{table_name}'.")
        raise
    finally:
        cur.close()
        conn.close()


def fetch_data(table_name: str, n_lines: int = 0) -> pd.DataFrame:
    """Fetch data from a table in the PostgreSQL database."""

    conn = connect()
    query = f"SELECT * FROM {table_name}"

    query += f" LIMIT {n_lines};" if n_lines > 0 else ";"

    try:
        warnings.simplefilter(action="ignore", category=UserWarning)
        df = pd.read_sql(query, conn)
        return df
    except Exception:
        print(f"Error fetching data from '{table_name}'.")
        raise
    finally:
        conn.close()


def delete_table(table_name: str) -> None:
    """Delete a table from the PostgreSQL database."""

    conn = connect()
    cur = conn.cursor()

    query = f"DROP TABLE {table_name};"

    try:
        cur.execute(query)
        conn.commit()
        print(f"Table '{table_name}' deleted successfully.")
    except Exception:
        conn.rollback()
        print(f"Error deleting table '{table_name}'.")
        raise
    finally:
        cur.close()
        conn.close()
