import ConfigParser
from osc.settings.base_settings import *

SECRETS_PATH = os.path.join(BASE_DIR, 'settings/dev/secrets.ini')

secrets = ConfigParser.ConfigParser()
secrets.read(SECRETS_PATH)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.get('django', 'SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
DEBUG = True
ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = (
    'localhost:3000'
)

ELASTICSEARCH = {
    'chunk_size': 100,
    'host': 'elastic.opensmartcountry.com',
    'port': 443,
    'use_ssl': True
}

GOOGLE = {
    'chunk_size': 512,
    'elevation_api_key': get_secret(secrets, 'Google Elevation', 'api_key'),
    'auth_client_id': get_secret(secrets, 'Google Auth', 'client_id'),
    'auth_client_secret': get_secret(secrets, 'Google Auth', 'client_secret'),
}

FACEBOOK = {
    'auth_app_id': get_secret(secrets, 'Facebook Auth', 'app_id'),
    'auth_app_secret': get_secret(secrets, 'Facebook Auth', 'app_secret'),
}

INFORIEGO = {
    'url.daily': 'http://www.inforiego.org/opencms/rest/diario',
    'index': 'inforiego',
    'daily.mapping': 'info_riego_daily',
    'station.mapping': 'info_riego_station',
    'user': get_secret(secrets, 'inforiego', 'user'),
    'passwd': get_secret(secrets, 'inforiego', 'passwd')
}

CADASTRE = {
    'index': 'parcels',
    'mapping': 'parcel',
    'zone.for.queries': 'EPSG::25830',
    'query.cadastre.when.bbox': True,
    'max.query.size': 5000
}

WEATHER = {
    'index': 'weather_v1',
    'weather.mapping': 'weather',
    'locations.mapping': 'locations',
    'owm_token': get_secret(secrets, 'openweathermap', 'token'),
    'owm_chunk_size': 60,
    'owm_chunk_time': 60
}

SOIL = {
    'index': 'soil',
    'mapping': 'soil'
}

SLACK = {
    'token': get_secret(secrets, 'slack', 'token'),
    'flush_bucket': 200
}

WEB = {
    'url': 'http://localhost:8000'
}

AUX_DIRS = {
    'data_dir': os.path.join(BASE_DIR, 'tmp/data'),
    'tmp_dir': os.path.join(BASE_DIR, 'tmp/tmp'),
    'log_dir': os.path.join(BASE_DIR, 'tmp/logs'),
    'errors_dir': os.path.join(BASE_DIR, 'tmp/errors'),
    'dataframes_dir': os.path.join(BASE_DIR, 'tmp/data_frames')
}

for dir_name in AUX_DIRS:
    if not os.path.exists(AUX_DIRS[dir_name]):
        os.makedirs(AUX_DIRS[dir_name])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'osc': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

TIME_ZONE = 'Europe/Madrid'
