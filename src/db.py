from pandas import DataFrame, read_csv, read_sql
from psycopg2 import connect
from psycopg2.errors import UndefinedTable
from psycopg2.extensions import connection
from psycopg2.extras import execute_values
from warnings import simplefilter

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASS,
    DATA_TABLE,
    INITIAL_DATA_FILE,
)
from utils import generate_create_table_query


def create_connection() -> connection:
    """Create a connection instance to the PostgreSQL database."""

    try:
        conn = connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
        )
        print("Connected to database.")
        return conn
    except Exception:
        print("Error connecting to database.")
        raise


def create_table(
    table_name: str, df: DataFrame = None, columns: list[tuple] = None
) -> None:
    """Create a table with the given name and data columns."""

    conn = create_connection()
    cur = conn.cursor()

    if table_exists(table_name):
        return

    if df is not None:
        query = generate_create_table_query(table_name, df=df)
    elif columns is not None:
        query = generate_create_table_query(table_name, columns=columns)
    else:
        print("No data or columns provided.")
        raise ValueError

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


def delete_table(table_name: str) -> None:
    """Delete a table with the given name if it exists."""

    if not table_exists(table_name):
        return

    conn = create_connection()
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


def table_exists(table_name: str) -> bool:
    """Check if a table exists."""

    conn = create_connection()
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
        (
            print(f"Table '{table_name}' exists.")
            if exists
            else print(f"Table '{table_name}' does not exist.")
        )
        return exists
    except Exception:
        print("Error checking if table exists.")
        return False
    finally:
        cur.close()
        conn.close()


def table_has_data(table_name: str) -> bool:
    """Check if a table has inserted data."""

    conn = create_connection()
    cur = conn.cursor()

    query = f"SELECT COUNT(*) FROM {table_name};"

    try:
        cur.execute(query)
        count = cur.fetchone()[0]
        print("Table has data.") if count > 0 else print("Table has no data.")
        return count > 0
    except UndefinedTable:
        print(f"Table '{table_name}' does not exist.")
        return False
    except Exception:
        print(f"Error checking if table '{table_name}' has data.")
        return False
    finally:
        cur.close()
        conn.close()


def insert_data(
    table_name: str, df: DataFrame = None, data: dict | list[dict] = None
) -> None:
    """Insert data from a pandas DataFrame or a dict into a table."""

    if df is None and data is None:
        print("No data provided.")
        raise ValueError

    if not table_exists(table_name):
        return

    conn = create_connection()
    cur = conn.cursor()

    if df is not None:
        values = [tuple(x) for x in df.to_numpy()]
        cols = ",".join(f'"{col}"' for col in df.columns)
        query = f"INSERT INTO {table_name} ({cols}) VALUES %s"

    elif data is not None:
        cols = [f'"{col}"' for col in data.keys()]
        placeholders = ", ".join([f"%({col.strip('\"')})s" for col in data.keys()])
        query = (
            f'INSERT INTO "{table_name}" ({", ".join(cols)}) VALUES ({placeholders})'
        )

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


def insert_initial_data() -> None:
    """Insert initial data into the database if the table is empty or does not exist."""

    if not table_exists(DATA_TABLE) or not table_has_data(DATA_TABLE):
        df = read_csv(INITIAL_DATA_FILE)

        if not table_exists(DATA_TABLE):
            create_table(DATA_TABLE)

        insert_data(DATA_TABLE, df=df)
        print("Initial data inserted.")
    else:
        print("Initial data already exists.")


def delete_data(table_name: str) -> None:
    """Delete all data from a table."""

    if not table_has_data(table_name):
        return

    conn = create_connection()
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


def fetch_data(
    table_name: str, n_lines: int = 0, desc_order: bool = False
) -> DataFrame | None:
    """Generate a dataframe with all or a specified number of lines fetched from a table in ascending or descending order."""

    if not table_has_data(table_name):
        return None

    conn = create_connection()

    query = f"SELECT * FROM {table_name} ORDER BY ctid"
    query += " DESC" if desc_order else " ASC"
    query += f" LIMIT {n_lines};" if n_lines > 0 else ";"

    try:
        simplefilter(action="ignore", category=UserWarning)
        df = read_sql(query, conn)
        print(f"Data fetched from '{table_name}' successfully.")
        return df
    except Exception:
        print(f"Error fetching data from '{table_name}'.")
        raise
    finally:
        conn.close()
