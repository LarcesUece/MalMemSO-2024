from flask import Flask


def create_app():
    app = Flask(__name__)
    app.logger.info("App created.")

    with app.app_context():
        from . import (
            analysis,
            classification,
            config,
            db,
            dumps,
            models,
            reports,
            routes,
            templates,
            training,
            utils,
            volmemlyzer,
        )
        from .db import initial_data

        app.config.from_object(config.Config)
        app.logger.info("Config loaded.")
        db.db.init_app(app)
        app.logger.info("Database initialized.")
        # db.db.drop_all()
        # app.logger.info("Database dropped.")
        db.db.create_all()
        app.logger.info("Database created.")
        initial_data.insert_initial_data()
        app.logger.info("Initial data inserted.")
        volmemlyzer.init_lib()
        app.logger.info("VolMemLyzer initialized.")

    return app
