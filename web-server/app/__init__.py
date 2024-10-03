import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

from app.config import DevelopmentConfig, ProductionConfig
from app.logger import create_logger

# Create a single SQLAlchemy instance
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config.from_object(__name__)

    with app.app_context():
        logger = create_logger(__name__)
        current_app.logger = logger
        current_app.bcrypt = Bcrypt(app)
        current_app.socketio = SocketIO(app, cors_allowed_origins="*")

    # Create all tables if not already created
    db.init_app(app)
    with app.app_context():
        from app.models import Containers, Users
        db.create_all()

        login_manager.login_view = 'main.login'
        login_manager.login_message = None
        login_manager.login_message_category = 'info'
        login_manager.init_app(app)

    # Imported later to prevent circular import
    from app.routes.main import main
    app.register_blueprint(main)

    return app
