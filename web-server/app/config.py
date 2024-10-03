import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'glorp')
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    LOGS_DIR = f'./logs/{LOG_LEVEL}.logs'

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    DATABASE_URI = 'sqlite:///development-webdude.db'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///production-webdudue.db')

