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

SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://tabiodun:6wEq6bmPiEA5@198.57.223.4/cbs'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

SENTRY_DSN = (
    'https://bca707435206403e94ad6667944db991:d976cff862db493b810ee08aede93ce2@'
    'sentry.io/1201842')
