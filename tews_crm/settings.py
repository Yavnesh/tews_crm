import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k@#pib9$j)va($^d643wcpn2-#!in&1i!s0p8kzpy&b9^mxklb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', 'now.sh', 'localhost', 'leapcell.io', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crm',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tews_crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tews_crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'railway',
#         'USER': 'postgres',
#         'PASSWORD': 'CESSzRbLJgwBZosfpMxufjsyjuauUXHb',
#         'HOST': 'roundhouse.proxy.rlwy.net',
#         'PORT': '39774',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Disable Browsable API in Production
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer',]
}


# Celery configuration
# Celery configuration using Redis broker and backend

#local server
# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Adjust port if needed
# CELERY_RESULT_BACKEND = 'django-db'

# for docker server
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")


# CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'  # Separate database for task results

# # postgresql
# result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'


CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_RESULT_EXTENDED = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# Optional settings for concurrency and queue management
# CELERY_ACKS_LATE = True
# CELERY_CONCURRENCY = 2  # Adjust for number of worker processes
# CELERY_IMPORTS = (
#     'crm.tasks',
# )




##############  Load environment variables  #######################

# Load environment variables from .env file
# env_path = Path('.') / '.env'
# Load environment variables from a .env file if available
# load_dotenv(dotenv_path=env_path)


# TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
# TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
# TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
# TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
# GEMINI_API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
# GEMINI_API_KEY_2 = os.getenv("GEMINI_API_KEY_2")
# GEMINI_API_KEY_3 = os.getenv("GEMINI_API_KEY_3")
# STABLE_HORDE_API_KEY = os.getenv("STABLE_HORDE_API_KEY")


# Twitter Credentials

TWITTER_CONSUMER_KEY="n6WhBu3WFF3OU0qwEDwD1Zrza"
TWITTER_CONSUMER_SECRET="kjvqKWucaPNfFAFhT8y1HdbDFr00uiIHqU1uQ6gPCsCh6MznJ8"
TWITTER_ACCESS_TOKEN="1784831051531243520-GlRNKbdW59CgM2hm91MJUn5JyaY2t2"
TWITTER_ACCESS_TOKEN_SECRET="ZWrMnCCUyouuWxYkxEGW3rws3pL8SACvR7jW8Pl1EZEVx"

# Google Gemini Credentials

GEMINI_API_KEY_1="AIzaSyBJaCAFmsYpMcO7OTNEJV6I-Ci9O7-X03Q"
GEMINI_API_KEY_2="AIzaSyAZLlvQ2yyZxQ6WqfZ0uTBKIhVxU0c-Ml8"
GEMINI_API_KEY_3="AIzaSyDmNszyVZrJ-2q2jwVwSsn7Opt0KhjTlGU"

# Horde Credentials

STABLE_HORDE_API_KEY="7LGsqLjIsFMXtsnwbgobTA"
