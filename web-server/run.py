import os

from app import create_app
from app.config import DevelopmentConfig, ProductionConfig

app = create_app(config=DevelopmentConfig)

if __name__ == "__main__":
    app.socketio.run(app, debug=True, port=5000, host="0.0.0.0")