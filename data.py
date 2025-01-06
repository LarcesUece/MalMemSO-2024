import psycopg2
import pandas as pd
import os


def write_initial_data():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")

    conn = psycopg2.connect(
        dbname=database, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()
    table_name = "malmemso_data"

    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    if count > 0:
        print("Data already exists in the database.")
        return

    files = []
    data_dir = "data"

    for file in os.listdir(data_dir):
        files.append(pd.read_csv(os.path.join(data_dir, file)))

    combined_df = pd.concat(files, ignore_index=True)
    columns = combined_df.columns.tolist()
    insert_query = f"""
    INSERT INTO {table_name} ({', '.join(columns)})
    VALUES ({', '.join(['%s'] * len(columns))})"""

    for i, row in combined_df.iterrows():
        cur.execute(insert_query, tuple(row))

    conn.commit()
    cur.close()
    conn.close()

    print("Initial data written to database.")
