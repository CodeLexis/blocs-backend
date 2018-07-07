import os


BROKER_URL = 'redis://localhost:6379'
CELERY_INCLUDE = ['tasks']
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'tomisin.abiodun@techadvance.ng'
MAIL_PASSWORD = 'iamexcellent'
MAIL_SENDER_NAME = 'CBA'
MAIL_SENDER_ADDRESS = 'tomisin.abiodun@techadvance.ng'

SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://tomisin:tomisin10@localhost/blocs_development'
)

# if os.environ['RUNNING_MODE'] == 'production':
SQLALCHEMY_DATABASE_URI = (
    'postgres://eunvkeurmtiqms:'
    '040f7c59537f4966783680490afd00e79eca1d76ec316825a1217fe8df71d7d3@'
    'ec2-184-73-199-189.compute-1.amazonaws.com:5432/deg37l3nadk5ri'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

SENTRY_DSN = (
    'https://bca707435206403e94ad6667944db991:d976cff862db493b810ee08aede93ce2@'
    'sentry.io/1201842')
