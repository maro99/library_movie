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



# Media
DEFAULT_FILE_STORAGE = "config.storages.S3DefaultStorage"
AWS_STORAGE_BUCKET_NAME = secrets["AWS_STORAGE_BUCKET_NAME"]