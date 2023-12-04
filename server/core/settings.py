from corsheaders.defaults import default_headers
from pathlib import Path
import os
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent



deploy = True
if(deploy):
    # deploy
    SECRET_KEY = os.getenv('SECRET_KEY', 'LIARA_URL is not set.')
    DEBUG = os.getenv('DEBUG', 'LIARA_URL is not set.')
else:
    # local
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = True

ALLOWED_HOSTS = ["*","89.199.35.132","192.168.45.68",]
CORS_ORIGIN_ALLOW_ALL=True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
]


INSTALLED_APPS += [
    'info',
]

CORS_ALLOWED_ORIGINS = [
    "chrome-extension://eipdnjedkpcnlmmdfdkgfpljanehloah",
]

# CSRF_TRUSTED_ORIGINS = [
#     "chrome-extension://eipdnjedkpcnlmmdfdkgfpljanehloah",
# ]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # +++
    'django.middleware.common.CommonMiddleware',  # +++
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'core.urls'


MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'react/build')],
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



WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# SQLITE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
# STATIC_ROOT =  os.path.join(BASE_DIR, 'static/')



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

