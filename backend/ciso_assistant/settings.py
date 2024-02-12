"""
Django settings for ciso_assistant project.

CORS are not managed by backend, so CORS library is not used

if "POSTGRES_NAME" environment variable defined, the database engine is posgresql
and the other env variables are POSGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT
else it is sqlite, and no env variable is required

"""

from pathlib import Path
import os
import json
from urllib.parse import urlparse
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

print("BASE_DIR:", BASE_DIR)

with open(BASE_DIR / "ciso_assistant/VERSION") as f:
    VERSION = f.read().strip()
    print(f"CISO Assistant Version: {VERSION}")

try:
    with open(BASE_DIR / "ciso_assistant/build.json") as f:
        BUILD = json.load(f)["build"]
except FileNotFoundError:
    BUILD = "unset"
    print("CISO Assistant Build: unset. Please refer to the documentation to set it.")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG") == "True"

print("DEBUG mode:", DEBUG)
CISO_ASSISTANT_URL = os.environ.get("CISO_ASSISTANT_URL", "http://localhost:5173")
print("CISO_ASSISTANT_URL:", CISO_ASSISTANT_URL)
# ALLOWED_HOSTS should contain the backend address
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
print("ALLOWED_HOSTS", ALLOWED_HOSTS)
CSRF_TRUSTED_ORIGINS = [CISO_ASSISTANT_URL]
LOCAL_STORAGE_DIRECTORY = os.environ.get(
    "LOCAL_STORAGE_DIRECTORY", BASE_DIR / "db/attachments"
)
ATTACHMENT_MAX_SIZE_MB = os.environ.get("ATTACHMENT_MAX_SIZE_MB", 10)
MEDIA_ROOT = LOCAL_STORAGE_DIRECTORY
MEDIA_URL = ""

PAGINATE_BY = os.environ.get("PAGINATE_BY", default=500)


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.forms",
    "tailwind",
    "iam",
    "core",
    "cal",
    "django_filters",
    "library",
    "serdes",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ciso_assistant.urls"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

SESSION_COOKIE_AGE = int(
    os.environ.get("SESSION_COOKIE_AGE", default=60 * 15)
)  # defaults to 15 minutes
# prevents session from expiring when user is active
SESSION_SAVE_EVERY_REQUEST = os.environ.get("SESSION_SAVE_EVERY_REQUEST", default=True)
SESSION_EXPIRE_AT_BROWSER_CLOSE = os.environ.get(
    "SESSION_EXPIRE_AT_BROWSER_CLOSE", default=True
)

CISO_ASSISTANT_SUPERUSER_EMAIL = os.environ.get("CISO_ASSISTANT_SUPERUSER_EMAIL")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
# rescue mail
EMAIL_HOST_RESCUE = os.environ.get("EMAIL_HOST_RESCUE")
EMAIL_PORT_RESCUE = os.environ.get("EMAIL_PORT_RESCUE")
EMAIL_HOST_USER_RESCUE = os.environ.get("EMAIL_HOST_USER_RESCUE")
EMAIL_HOST_PASSWORD_RESCUE = os.environ.get("EMAIL_HOST_PASSWORD_RESCUE")
EMAIL_USE_TLS_RESCUE = os.environ.get("EMAIL_USE_TLS_RESCUE")

EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", default="5"))  # seconds

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "core.permissions.RBACPermissions",
    ],
    "DEFAULT_FILTER_CLASSES": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": PAGINATE_BY,
}

# templates are still used to send email
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
    "rest_framework.renderers.BrowsableAPIRenderer"
)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "ciso_assistant.wsgi.application"

AUTH_USER_MODEL = "iam.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
]

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

LOCALE_PATHS = (os.path.join(PROJECT_PATH, "../locale"),)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if "POSTGRES_NAME" in os.environ:
    print("Postgresql database engine")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ["POSTGRES_NAME"],
            "USER": os.environ["POSTGRES_USER"],
            "PASSWORD": os.environ["POSTGRES_PASSWORD"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
    print("Postgresql database engine")
else:
    print("sqlite database engine")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db/ciso-assistant.sqlite3",
        }
    }

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]
