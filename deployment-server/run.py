import os

from server import create_server
from server.config import DevelopmentConfig, ProductionConfig

app = create_server(config=DevelopmentConfig)

if __name__ == "__main__":
    app.run(debug=True, port=10000, host="0.0.0.0")