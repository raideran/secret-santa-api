import os
from datetime import timedelta


def setup_db_uri():
    dbpath = os.path.normpath('../database.db')
    url = f'sqlite:///{dbpath}'
    return url


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ukf4H5dn9x6lbmhc0yJ2blqvQuUpFBbuw5nRM+BcKyM='
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'ukf4H5dn9x6lbmhc0yJ2blqvQuUpFBbuw5nRM+BcKyM='
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = setup_db_uri()


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = setup_db_uri()


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
