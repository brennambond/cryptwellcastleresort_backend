import os
import dj_database_url

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RUNNING_IN_GITLAB = os.getenv('GITLAB_CI') == 'true'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'cryptwellcastleresort-backend.onrender.com',
]


AUTH_USER_MODEL = 'useraccount.User'

SITE_ID = 1

WEBSITE_URL = os.getenv("WEBSITE_URL", "http://localhost:8000")

CSRF_TRUSTED_ORIGINS = ['http://35.170.218.30',
                        'https://hauntedhotel-backend-api.com', 'http://hauntedhotel-backend-api.com', 'https://thecryptwellcastleresort.vercel.app', 'https://cryptwellcastleresort-backend.onrender.com',]


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKEN": True,
    "BLACKLIST_AFTER_ROTATION": True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    "UPDATE_LAST_LOGIN": True,
    "SIGNIN_KEY": 'acomplexkey',
    'ALGORITHM': 'HS256',
}

SESSION_COOKIE_SECURE = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Cryptwell Castle Resort',
    'DESCRIPTION': 'Hotel Booking API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://thecryptwellcastleresort.vercel.app",
    'https://cryptwellcastleresort-backend.onrender.com',
]


CORS_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    'http://0.0.0.0:8000',
    'http://0.0.0.0:80',
    'http://0.0.0.0:3000',
    'http://0.0.0.0',
    'http://0.0.0.0:1337',
    'https://hauntedhotel.vercel.app',
    'http://hauntedhotel.vercel.app',
]

CORS_ORIGINS_WHITELIST = [
    'http://0.0.0.0:8000',
    'http://0.0.0.0:80',
    'http://0.0.0.0:3000',
    'http://0.0.0.0',
    'http://0.0.0.0:1337',
    'https://hauntedhotel.vercel.app',
    'http://hauntedhotel.vercel.app',
]


REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
}


INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',


    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'dj_rest_auth',
    'dj_rest_auth.registration',
    'drf_spectacular',

    'corsheaders',

    'storages',

    'room',
    'useraccount',
    'reservations',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hh_api.urls'

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

WSGI_APPLICATION = 'hh_api.wsgi.application'
ASGI_APPLICATION = 'hh_api.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if RUNNING_IN_GITLAB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'test_db'),
            'USER': os.getenv('POSTGRES_USER', 'test_user'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'test_pass'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_AKI')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SAK')

# AWS_STORAGE_BUCKET_NAME = os.environ.get(
#     'AWS_SBN', "hauntedhotel-backend-bucket")
# print("AWS_STORAGE_BUCKET_NAME:", AWS_STORAGE_BUCKET_NAME)
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.us-east-1.amazonaws.com"
# print("AWS_S3_CUSTOM_DOMAIN:", AWS_S3_CUSTOM_DOMAIN)

# AWS_S3_FILE_OVERWRITE = True

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
#     },

#     "staticfiles": {
#         "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
#     }
# }

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }
}
