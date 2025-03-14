from flask import Flask
from .extentions import db, migrate
from .config import Config


def create_app(config_class=Config) -> Flask(__name__):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
