from psycopg2.extensions import connection
from pandas import DataFrame

from .. import db

table_name = "test_table"
columns = {
    "id": "SERIAL PRIMARY KEY",
    "name": "VARCHAR(255) NOT NULL",
    "age": "INTEGER NOT NULL",
}
df = DataFrame(
    {
        "name": ["Alice", "Bob"],
        "age": [25, 30],
    }
)
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
]


def test_create_connection():
    assert isinstance(db.create_connection(), connection)
    assert db.create_connection().closed == 0


def test_create_table():
    db.create_table(table_name, columns=columns)
    assert db.table_exists(table_name)
    assert not db.table_has_data(table_name)
    db.delete_table(table_name)
    db.create_table(table_name, df=df)
    assert db.table_exists(table_name)
    assert not db.table_has_data(table_name)
    db.delete_table(table_name)


def test_insert_data():
    db.create_table(table_name, columns=columns)
    db.insert_data(table_name, data=data)
    assert db.table_has_data(table_name)
    assert db.fetch_data(table_name) == df
    db.delete_data(table_name)
    db.insert_data(table_name, df=df)
    assert db.table_has_data(table_name)
    assert db.fetch_data(table_name) == df
    db.delete_table(table_name)


def test_table_exists():
    assert not db.table_exists(table_name)
    db.create_table(table_name, columns=columns)
    assert db.table_exists(table_name)
    db.delete_table(table_name)
    assert not db.table_exists(table_name)


def test_table_has_data():
    assert not db.table_has_data(table_name)
    db.create_table(table_name, df=df)
    assert not db.table_has_data(table_name)
    db.insert_data(table_name, df=df)
    assert db.table_has_data(table_name)
    db.delete_table(table_name)


def test_insert_initial_data():
    db.insert_initial_data()
    assert db.table_has_data(db.config.DATA_TABLE)
    db.delete_data(db.config.DATA_TABLE)
    db.insert_initial_data()
    assert db.table_has_data(db.config.DATA_TABLE)
    db.delete_data(db.config.DATA_TABLE)


def test_delete_data():
    db.create_table(table_name, df=df)
    db.insert_data(table_name, df=df)
    db.delete_data(table_name)
    assert not db.table_has_data(table_name)
    db.delete_table(table_name)


def test_fetch_data():
    db.create_table(table_name, df=df)
    db.insert_data(table_name, df=df)
    assert db.fetch_data(table_name) == df
    db.delete_table(table_name)


def test_delete_table():
    db.create_table(table_name, df=df)
    db.delete_table(table_name)
    assert not db.table_exists(table_name)
    db.create_table(table_name, df=df)
    db.delete_table(table_name)
    assert not db.table_exists(table_name)
