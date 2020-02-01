import os
from datetime import timedelta
from dotenv import load_dotenv

from app.utils import CustomJSONEncoder

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWTs
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'imasosecret')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=120)
    # token revoking
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True

    # Flask-admin
    FLASK_ADMIN_SWATCH = 'cerulean'

    CORS_HEADERS = 'Content-Type'

    RESTFUL_JSON = {'separators': (', ', ': '),
                    'indent': 2,
                    'cls': CustomJSONEncoder}


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    TESTING = True
