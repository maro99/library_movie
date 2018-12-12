from .base import *
import sys
secrets = json.load(open(os.path.join(SECRET_DIR,'production.json')))

RUNSERVER = 'runserver' in sys.argv
DEBUG = False
ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

if RUNSERVER:
    DEBUG = True
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
    ]


WSGI_APPLICATION = 'config.wsgi.production.application'
INSTALLED_APPS += [
    'storages',
]

# DB
DATABASES = secrets['DATABASES']


# CELERY + Redis  #local에서
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# # CELERY + Redis  # dev docker에서 elasticache말고 자체 캐시 쓸때
# CELERY_BROKER_URL = 'redis://0'
# CELERY_RESULT_BACKEND = 'redis://0'

#CELERY + Redis
CELERY_BROKER_URL = 'redis://'+ AWS_ELASTIC_CACHE
CELERY_RESULT_BACKEND = 'redis://' + AWS_ELASTIC_CACHE


# CELERY_BEAT
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TAST_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul' #Celery beat가 스케줄러이기 때문에 시간에 대한 정의를 해야함



# Media
DEFAULT_FILE_STORAGE = "config.storages.S3DefaultStorage"
AWS_STORAGE_BUCKET_NAME = secrets["AWS_STORAGE_BUCKET_NAME"]


LOG_DIR = '/var/log/django'
if not os.path.exists(LOG_DIR):
    LOG_DIR = os.path.join(ROOT_DIR, '.log')
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'django.server',
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10485760,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_error'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}