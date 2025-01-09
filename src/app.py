from src import create_app

import db
import model

app = create_app()


def initialize():
    db.insert_initial_data()
    model.initialize()


if __name__ == "__main__":
    initialize()
    app.run(host="0.0.0.0", port=5002)
