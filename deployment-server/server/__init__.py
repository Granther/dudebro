import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from server.config import DevelopmentConfig, ProductionConfig
from server.logger import create_logger

# Create a single SQLAlchemy instance
db = SQLAlchemy()

def create_server(config=DevelopmentConfig):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config.from_object(__name__)

    with app.app_context():
        logger = create_logger(__name__, config)
        current_app.logger = logger
        current_app.bcrypt = Bcrypt(app)

    # Create all tables if not already created
    db.init_app(app)
    with app.app_context():
        from server.models import GameTypes
        db.create_all()

    # Imported later to prevent circular import
    from server.routes.main import main
    app.register_blueprint(main)

    return app
