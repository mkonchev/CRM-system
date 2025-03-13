from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sqlalchemy.model import DefaultMeta

db = SQLAlchemy()
migrate = Migrate()
