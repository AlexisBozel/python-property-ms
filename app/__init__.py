from flask import Flask
from .api.endpoints.property import property_blueprint
from .api.endpoints.room import room_blueprint
from .api.endpoints.pricing import pricing_blueprint
from .api.endpoints.advert import advert_blueprint
from .dependencies import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings.DevelopmentConfig')

    # Registering blueprints
    app.register_blueprint(property_blueprint)
    app.register_blueprint(room_blueprint)
    app.register_blueprint(pricing_blueprint)
    app.register_blueprint(advert_blueprint)
    init_db(app.config)

    return app
