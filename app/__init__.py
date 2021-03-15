from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.helpers import CustomJSONEncoder


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json_encoder = CustomJSONEncoder

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.main import models

    return app
