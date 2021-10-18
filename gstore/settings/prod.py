from .common import *
import json
from django.core.exceptions import ImproperlyConfigured
import os

# with open("secret.json") as f:
#     secrets = json.loads(f.read())

# def get_secret(setting):
#     # 비밀 변수를 가져오거나 명시적 예외를 반환한다.
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = f'Set the {setting} environment variable'
#         raise ImproperlyConfigured(error_msg)

DEBUG = os.environ.get("DEBUG") in ["1", "t", "true", "T", "True"]
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")


STATICFILES_STORAGE = "gstore.storages.StaticAzureStorage"

AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]


# CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")


DATABASES = {
    "default": {
        "ENGINE": os.environ["DB_ENGINE"],
        "HOST": os.environ["DB_HOST"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "NAME": os.environ["DB_NAME"],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "ERROR", "class": "logging.StreamHandler",},},
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR",},},
}