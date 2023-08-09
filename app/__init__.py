from flask import Flask

from app.blueprints.api_bp import api_bp
from app.blueprints.rendering_bp import rendering_bp
from app.blueprints.static_files_bp import static_files_bp
from app.config import Config
from app.db.database import db
from flask_migrate import Migrate, upgrade


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(config_class)

    process_migrations(app)
    register_blueprints(app)

    return app


def process_migrations(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        upgrade()


def register_blueprints(app):
    app.register_blueprint(static_files_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(rendering_bp)
