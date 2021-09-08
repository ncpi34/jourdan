from app.settings import MIDDLEWARE
'''''''''
'' LOGS''
'''''''''
# pip install django-crum
# python manage.py makemigrations log_db
# python manage.py migrate
MIDDLEWARE += ['crum.CurrentRequestUserMiddleware']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'get_user': {
            '()': 'log_db.filters.ContextFilter',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        # 'console': {
        #     'level': 'DEBUG',
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'simple'
        # },
        'db': {

            'class': 'log_db.handlers.DatabaseLogHandler',
            'filters': ['get_user'],
            'formatter': 'simple'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}

