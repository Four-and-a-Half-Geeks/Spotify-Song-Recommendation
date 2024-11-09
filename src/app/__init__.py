from flask import Flask
from .routes import main_blueprint
from .config import Config

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    # Register blueprints (routes)
    app.register_blueprint(main_blueprint)

    return app