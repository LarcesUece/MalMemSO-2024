from flask import Flask

from db import insert_initial_data
from model import initialize as init_model


def create_app() -> Flask:
    """Create a Flask app instance and import necessary modules."""

    app = Flask(__name__)

    with app.app_context():
        import routes

    return app


def initialize():
    """Inialize the databases."""

    insert_initial_data()
    init_model()
