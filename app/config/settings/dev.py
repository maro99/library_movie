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

# Media
DEFAULT_FILE_STORAGE = "config.storages.S3DefaultStorage"
AWS_STORAGE_BUCKET_NAME = secrets["AWS_STORAGE_BUCKET_NAME"]