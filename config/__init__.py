"""Default Configuration"""
import logging


class BaseConfig(object):
    # temp dirty config
    HOST_IP = '0.0.0.0'
    HOST_PORT = 1234

    ###################
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret-key-to-be-changed'

    RECEIPT_BASE = 31415926535897


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # SQLALCHEMY_DATABASE_URI = (
    #     'mysql+pymysql://acetakwas:password@127.0.0.1/phed_test'
    # )
    # SQLALCHEMY_BINDS = {
    #     'billing_system':
    #         'mysql+pymysql://acetakwas:password@127.0.0.1/billing_system'
    # }


class PilotConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    # best be explicit
    DEBUG = False
    TESTING = False

    ##################
    # RECEIPT SEED!!!!
    # DO NOT CHANGE!!!
    RECEIPT_BASE = 210213134115000130  # DO NOT CHANGE!!!
    # DO NOT CHANGE!!!
    ##################

    FILE_LOG_LEVEL = logging.WARN
    CONSOLE_LOG_LEVEL = logging.WARN


config_modes = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'pilot': PilotConfig,
    'production': ProductionConfig
}


def load_configuration(app, mode):
    configuration = config_modes[mode]
    app.config.from_object(configuration)
    app.config.from_pyfile('config.py', silent=True)
