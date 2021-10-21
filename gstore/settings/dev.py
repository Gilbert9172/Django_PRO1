from .common import *

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware",] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'gstore' ,'static')
]

CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]