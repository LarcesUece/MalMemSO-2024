import time

import db
import config
import model


def initialize():
    # db.delete_table(config.DATA_TABLE)
    # db.delete_table(config.MODEL_TABLE)
    # db.insert_initial_data()
    # model.initialize()
    db1 = db.fetch_data(config.DATA_TABLE, n_lines=5)
    db2 = db.fetch_data(config.MODEL_TABLE, n_lines=5)
    print(db1.to_string())
    print(db2.to_string())


def run():
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    initialize()
    run()
