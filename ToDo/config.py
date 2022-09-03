from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DevelopmentConfig(object):
    """
    Development configuration just for local development
    """
    SQLALCHEMY_DATABASE_URI = f"sqlite:///todo_app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'


class TestingConfig(object):
    """ Testing configuration just for local development"""
    ...


class ProductionConfig(object):
    """ Deployment configuration for production development"""
    ...


APP_CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
