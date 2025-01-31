from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from . import config, db, routes, templates, views
        from .db import initial_data

        app.config.from_object(config.Config)
        db.db.init_app(app)
        # db.db.drop_all()
        db.db.create_all()
        initial_data.insert_initial_data()

    return app
