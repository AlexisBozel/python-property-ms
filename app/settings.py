import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    HOST = os.environ.get('DB_HOST', 'my-release-mysql.default.svc.cluster.local')
    USERNAME = os.environ.get('DB_USERNAME', 'root')
    PASSWORD = os.environ.get('DB_PASSWORD', 'my-root-password')
    PORT = os.environ.get('DB_PORT', '3307')
    DB_NAME = os.environ.get('DB_NAME', 'python_property_service')

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
