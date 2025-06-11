import os

SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe')
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'channels',
    'app.chat',
]

ROOT_URLCONF = 'app.urls'
ASGI_APPLICATION = 'app.asgi.application'

CHANNEL_LAYERS = {
    'default': { 'BACKEND': 'channels.layers.InMemoryChannelLayer' }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple_json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple_json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}