import pandas as pd
from datetime import datetime

from .. import utils

tz = "America/New_York"
table_name = "test_table"
df = pd.DataFrame(
    {
        "col1": [1, 2, 3],
        "col2": [1.0, 2.0, 3.0],
        "col3": [datetime.now(), datetime.now(), datetime.now()],
        "col4": ["a", "b", "c"],
    }
)
columns = [("col1", "INTEGER"), ("col2", "DOUBLE PRECISION")]


def test_map_pandas_to_postgres():
    assert utils.map_pandas_to_postgres(pd.Int64Dtype()) == "INTEGER"
    assert utils.map_pandas_to_postgres(pd.Float64Dtype()) == "DOUBLE PRECISION"
    assert utils.map_pandas_to_postgres(pd.DatetimeTZDtype(tz=tz)) == "TIMESTAMPTZ"
    assert utils.map_pandas_to_postgres(datetime.now()) == "TIMESTAMPTZ"
    assert (
        utils.map_pandas_to_postgres(datetime.now(utils.timezone(tz))) == "TIMESTAMPTZ"
    )
    assert utils.map_pandas_to_postgres(pd.StringDtype()) == "TEXT"


def test_generate_create_table_query():
    query = utils.generate_create_table_query(table_name, df=df)
    assert query == (
        'CREATE TABLE test_table ("col1" INTEGER, "col2" DOUBLE PRECISION, '
        '"col3" TIMESTAMPTZ, "col4" TEXT);'
    )
    query = utils.generate_create_table_query(table_name, columns=columns)
    assert query == 'CREATE TABLE test_table ("col1" INTEGER, "col2" DOUBLE PRECISION);'


def test_get_timestamp():
    assert utils.get_timestamp().tzinfo == utils.timezone(tz)
