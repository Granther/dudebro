import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'glorp')
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    LOGS_DIR = f'./logs/{LOG_LEVEL}.logs'

    ZONE_ID = os.environ.get('ZONE_ID')
    API_KEY = os.environ.get('API_KEY')
    DOMAIN = os.environ.get('DOMAIN')
    PUBLIC_IP = os.environ.get('PUBLIC_IP')
    EMAIL = os.environ.get('EMAIL')
    TARGET_FQDN = os.environ.get('TARGET_FQDN')

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    DATABASE_URI = 'sqlite:///development-dudeserver.db'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///production-dudeserver.db')

