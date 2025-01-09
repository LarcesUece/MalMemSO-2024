from time import sleep

import db
import model


def initialize():
    db.insert_initial_data()
    model.initialize()


def run():
    while True:
        sleep(3600)


if __name__ == "__main__":
    initialize()
    run()
