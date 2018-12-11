from .base import *

secrets = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))

DEBUG = True
ALLOWED_HOSTS = [

]

WSGI_APPLICATION = 'config.wsgi.dev.application'

INSTALLED_APPS += [
    'storages',
    'django_extensions'
]

# DB
DATABASES = secrets["DATABASES"]



# CELERY + Redis
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# CELERY_BEAT
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TAST_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul' #Celery beat가 스케줄러이기 때문에 시간에 대한 정의를 해야함



# Media
DEFAULT_FILE_STORAGE = "config.storages.S3DefaultStorage"
AWS_STORAGE_BUCKET_NAME = secrets["AWS_STORAGE_BUCKET_NAME"]