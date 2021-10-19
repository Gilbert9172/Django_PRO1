import os,json
from os.path import abspath, dirname
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

with open("secret.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    # 비밀 변수를 가져오거나 명시적 예외를 반환한다.
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓 SECRET_KEY 보호 〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
SECRET_KEY = get_secret('SECRET_KEY')

# 개발 모드
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Apps
    'bootstrap4',
    # 'debug_toolbar',

    # Local Apps
    'accounts',
    'buy',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'gstore' ,'templates')
        ],
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

WSGI_APPLICATION = 'gstore.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = { 
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql', 
#         'NAME': 'gstore',
#         'USER': 'gilbert917',
#         'PASSWORD' : '950904',
#         'HOST' : 'localhost',
#         'PORT' :'5432', } 
#         }



# User모델 재정의
AUTH_USER_MODEL = "accounts.User"

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



#〓〓〓〓〓〓〓〓〓〓〓〓〓〓 Static/Media 〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'gstore' ,'static')
# ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓 Login/Logout 〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'