"""The app module, containing the app factory function."""
from flask import Flask
from flask_cors import CORS

from app.routes import home, views, actions, formated_data, external
from app.extensions import db, migrate, login_manager
from app.services.net_and_connections import notify_new_public_ip


def create_app(config_object="app.config"):
    # Create application factory. Param config_object, the configuration object to use.
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    set_CORS(app)
    on_init()
    return app


def register_extensions(app):
    # Initialize the extensions.
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return None


def register_blueprints(app):
    # Register Flask blueprints.
    app.register_blueprint(home.home_bp)
    app.register_blueprint(views.views_bp)
    app.register_blueprint(actions.actions_bp)
    app.register_blueprint(formated_data.formated_data_bp)
    app.register_blueprint(external.external_bp)
    return None


def set_CORS(app):
    CORS(app, origins=['http://localhost:4200'])
    return None


def on_init():
    try:
        notify_new_public_ip()
    except:
        print('Init Error')