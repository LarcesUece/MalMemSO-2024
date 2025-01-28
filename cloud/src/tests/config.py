import os

from .. import config


def test_dirs():
    dirs = [config.SRC_DIR, config.ROOT_DIR, config.DATA_DIR]
    for dir in dirs:
        assert os.path.exists(dir)


def test_files():
    files = [config.INITIAL_DATA_FILE, config.ENV_FILE]
    for file in files:
        assert os.path.exists(file)


def test_tables():
    tables = [config.DATA_TABLE, config.MODEL_TABLE]
    for table in tables:
        assert len(table) > 0


def test_db_vars():
    db_vars = [
        config.DB_USER,
        config.DB_PASS,
        config.DB_HOST,
        config.DB_PORT,
        config.DB_NAME,
    ]
    for var in db_vars:
        assert isinstance(var, str)
        assert len(var) > 0


def test_model_columns():
    for col in config.MODEL_COLUMNS:
        assert len(col) == 2
        assert isinstance(col[0], str)
        assert len(col[0]) > 0
        assert isinstance(col[1], str)
        assert len(col[1]) > 0


def test_features_volmemlyzer():
    assert len(config.FEATURES_VOLMEMLYZER_V2) > 0
    assert len(config.FEATURES_VOLMEMLYZER_V2_2024) > 0
    assert len(config.FEATURES_VOLMEMLYZER_V2) == len(
        config.FEATURES_VOLMEMLYZER_V2_2024
    )
    for feature in config.FEATURES_VOLMEMLYZER_V2:
        assert isinstance(feature, str)
        assert len(feature) > 0
    for feature in config.FEATURES_VOLMEMLYZER_V2_2024:
        assert isinstance(feature, str) or feature is None
        assert len(feature) > 0


def test_timestamps():
    assert len(config.PYTZ_TIMEZONE) > 0


def test_training_algorithms():
    assert len(config.ALGORITHMS) > 0
    for algorithm in config.ALGORITHMS:
        assert isinstance(algorithm, str)
        assert len(algorithm) > 0
