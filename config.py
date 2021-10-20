import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # app config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    # db config
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # mail config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_USERNAME')

    # login config
    USE_SESSION_FOR_NEXT = True

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'test.db')

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'production.db')

config = {
    'test': TestConfig,
    'production': ProdConfig
}
