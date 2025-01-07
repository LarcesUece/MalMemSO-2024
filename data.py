import psycopg2
import pandas as pd
import os


def get_connection_to_db():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")

    conn = psycopg2.connect(
        dbname=database, user=user, password=password, host=host, port=port
    )

    return conn


def create_table(conn, df, table_name):
    cursor = conn.cursor()
    columns = ", ".join([f"{col} TEXT" for col in df.columns])
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        {columns}
    );"""
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()


def insert_data_into_table(conn, df, table_name):
    cursor = conn.cursor()

    for _, row in df.iterrows():
        columns = ", ".join(df.columns)
        values = ", ".join([f"'{str(v).replace('\'', '\'\'')}'" for v in row.values])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        cursor.execute(insert_query)

    conn.commit()
    cursor.close()


def is_table_empty(conn, table_name):
    cursor = conn.cursor()

    table_exists_query = f"""
    SELECT EXISTS (
        SELECT FROM pg_catalog.pg_class c
        JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = '{table_name}' AND c.relkind = 'r'
    );
    """
    cursor.execute(table_exists_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.close()
        return True

    check_empty_query = f"SELECT NOT EXISTS (SELECT 1 FROM {table_name} LIMIT 1);"
    cursor.execute(check_empty_query)
    result = cursor.fetchone()[0]
    cursor.close()
    return not result


def process_csv_to_df(data_dir):
    combined_data = pd.DataFrame()

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(data_dir, file_name)
            df = pd.read_csv(file_path)
            combined_data = pd.concat([combined_data, df], ignore_index=True)

    combined_data.columns = [col.replace(".", "_") for col in combined_data.columns]

    return combined_data


def write_initial_data():
    conn = get_connection_to_db()
    table_name = os.getenv("DATA_TABLE")

    if not is_table_empty(conn, table_name):
        conn.close()
        return

    data_dir = "initial_data"
    df = process_csv_to_df(data_dir)

    if not df.empty:
        create_table(conn, df, table_name)
        insert_data_into_table(conn, df, table_name)

    # print(fetch_first_five_rows(conn, table_name))
    # print(get_column_names(conn, table_name))

    conn.close()


# def fetch_first_five_rows(conn, table_name):
#     cursor = conn.cursor()
#     query = f"SELECT * FROM {table_name} LIMIT 5;"
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     cursor.close()
#     return rows


def fetch_data_from_db():
    table_name = os.getenv("DATA_TABLE")
    conn = get_connection_to_db()
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, conn)
    conn.close()
    return data


def get_column_names(conn, table_name):
    cursor = conn.cursor()
    query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = %s
    ORDER BY column_name;"""
    cursor.execute(query, (table_name,))
    columns = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return columns


def normalize_column_header(string=None, list=None):
    if list:
        new_list = []
        for item in list:
            if isinstance(item, str):
                new_list.append(normalize_column_header(item))
        return new_list

    if string:
        return string.replace(".", "_")

    return None
