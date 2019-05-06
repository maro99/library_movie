"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRET_DIR  = os.path.join(ROOT_DIR, '.secrets')
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secrets = json.load(open(os.path.join(SECRET_DIR, 'base.json')))
SECRET_KEY = secrets["SECRET_KEY"]

# Oauth
FACEBOOK_APP_ID = secrets['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET_CODE = secrets["FACEBOOK_APP_SECRET_CODE"]
KAKAOTALK_REST_API_KEY = secrets["KAKAOTALK_REST_API_KEY"]
NAVER_CLIENT_ID = secrets["NAVER_CLIENT_ID"]
NAVER_CLIENT_SECRET = secrets["NAVER_CLIENT_SECRET"]
GOOGLE_CLIENT_ID = secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = secrets["GOOGLE_CLIENT_SECRET"]
API_GOOGLE_CLIENT_ID = secrets["API_GOOGLE_CLIENT_ID"]
API_GOOGLE_CLIENT_SECRET = secrets["API_GOOGLE_CLIENT_SECRET"]

# Static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
# media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')


# AWS
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = secrets['AWS_DEFAULT_ACL']
AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = secrets['AWS_S3_SIGNATURE_VERSION']
AWS_ELASTIC_CACHE = secrets['AWS_ELASTIC_CACHE']


# SMS
SMS_API_KEY = secrets['SMS_API_KEY']
SMS_API_SECRET = secrets['SMS_API_SECRET']

# Auth
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pbkdf2_sha256$120000$aAwW76yogDKH$1rHLC3JH5MkKaXdQSAYIg+PIrtIc/X3MWqsROuad1Wc='
AUTH_USER_MODEL = 'members.User'
AUTHENTICATION_BACKENDS=[
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.SettingsBackend',  # 배포시 admin user로그인 시키고 마이그래이션 할때 사용
    'members.backends.FacebookBackend',  # 소셜로그인 각각 백엔드 만들어 진행 하려던것.for
    'members.backends.KakaotalkBackend',
    'members.backends.NaverBackend',
    'members.backends.GoogleBackend',
    "allauth.account.auth_backends.AuthenticationBackend", # alluath 관련

]

# alluath 관련
SITE_ID = 1
LOGIN_REDIRECT_URL = '/' # home


# DRF

# 기본적으로는 render를 html, json 두가지 경우 가능하게 하고 production 경우에는 browsableapirenderer 꺼주겠다.
DEFAULT_RENDERER_CLASSES =  (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
# username, password넣는 옵션.
 # test 서버에 들어있으면 좋음 (배포는 안넣는게맞음) 우리는 개발 배포 분리 못하니까 걍 들어있는 상태로 해라.
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',     # basic, sessoin, 이 기본이긴 하다.
        # 'rest_framework.authentication.SessionAuthentication', # ( api아닌 일반에서는 session쓰지만 이건 DRF관련 인증 설정이니지워도 된다.)
   ),
   'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}


# EMAIL SEND
EMAIL_BACKEND = secrets['EMAIL_BACKEND']
EMAIL_USE_TLS =secrets['EMAIL_USE_TLS']
EMAIL_PORT = secrets['EMAIL_PORT']
EMAIL_HOST = secrets['EMAIL_HOST']
EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PASSWORD']
SERVER_EMAIL = secrets['SERVER_EMAIL']
DEFAULT_FROM_MAIL = secrets['DEFAULT_FROM_MAIL']


# CORS

CORS_ORIGIN_ALLOW_ALL=False

CORS_ORIGIN_WHITELIST = (
    'localhost:3001',
    'localhost:3000',
    'localhost:8000',
    'maro5.com',
    'www.maro5.com',
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = default_headers + (
    'my-custom-header',
)



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
    'movies',

    'rest_framework',
    'rest_framework.authtoken',

    'celery',
    'django_celery_beat',
    'django_celery_results',

    # 이하 allauth관련
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True



