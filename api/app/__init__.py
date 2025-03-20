from flask import Flask
from .extentions import db, migrate
from .config import Config
from .models.users import Users
from .models.cars import Cars
from .models.orders import Orders


def create_app(config_class=Config):  # type: ignore
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
