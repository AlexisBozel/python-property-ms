from flask import Flask
from .api.endpoints.property import property_blueprint
from .dependencies import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings.DevelopmentConfig')

    # Registering blueprints
    app.register_blueprint(property_blueprint)
    init_db(app.config)

    return app
