import ConfigParser
from osc.settings.base_settings import *

SECRETS_PATH = os.path.join(BASE_DIR, 'tmp/secrets.ini')

secrets = ConfigParser.ConfigParser()
secrets.read(SECRETS_PATH)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.get('django', 'SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
DEBUG = False
ALLOWED_HOSTS = [u'oscapi', u'web', u'opensmartcountry.com', u'api.opensmartcountry.com']
USE_X_FORWARDED_HOST=True

# Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be
# marked as secure, which means browsers may ensure that the cookie is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = True

# Whether to use a secure cookie for the session cookie. If this is set to True, the cookie will be marked
#  as secure, which means browsers may ensure that the cookie is only sent under an HTTPS connection.
# Since its trivial for a packet sniffer (e.g. Firesheep) to hijack a users session if the session cookie
# is sent unencrypted, theres really no good excuse to leave this off. It will prevent you from using
# sessions on insecure requests and thats a good thing.
#SESSION_COOKIE_SECURE = True


#SECURE_SSL_REDIRECT = True

# A tuple representing a HTTP header/value combination that signifies a request is secure
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# As part of deploying your application youll need to run ./manage.py
# collectstatic to put all your static files into STATIC_ROOT
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise comes with a storage backend which automatically takes care of
# compressing your files and creating unique names for each version so they can
# safely be cached forever.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ELASTICSEARCH = {
    'chunk_size': 100,
    'host': 'elastic',
    'port': 9200,
    'use_ssl': False,
    'timeout': '60s',
    'retries': 3,
    'cluster_agg': {
        "2": {
            "geohash_grid": {
                "field": "properties.reference_point",
                "precision": 0
            },
            "aggs": {
                "area": {
                    "sum": {
                        "field": "properties.areaValue"
                    }
                }
            }
        }
    },
    'parcel_search_by_bbox': {
        "query": {
            "bool": {
                "filter": {
                    "geo_bounding_box": {
                        "properties.reference_point": {
                            "top": "",
                            "left": "",
                            "bottom": "",
                            "right": ""
                        }
                    }
                }
            }
        }
    },
    'parcel_search': {
        "query": {
        }
    }
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
    'cadastral_info_url': 'http://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx/Consulta_DNPRC',
    'url_inspire': 'http://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx',
    'url_atom_inspire': 'http://www.catastro.minhap.es/INSPIRE/CadastralParcels/ES.SDGC.CP.atom.xml',
    'index': 'parcels',
    'mapping': 'parcel',
    'zone.for.queries': 'EPSG::25830',
    'query.cadastre.when.bbox': False,
    'max.query.size': 5000
}

ITACYL = {
    'ITACYL_PROTOCOL': 'http://',
    'ITACYL_FTP': 'ftp.itacyl.es',
    'SIGPAC_PATH': 'cartografia/05_SIGPAC/2017_ETRS89/'
                   + 'Parcelario_SIGPAC_CyL_Municipios',
    'SIGPAC_FILE_DBF': 'RECFE.dbf'
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
    'flush_bucket': 1
}

WEB = {
    'url': 'https://opensmartcountry.com'
}

AUX_DIRS = {
    'data_dir': '/code/tmp/data',
    'tmp_dir': '/code/tmp/tmp',
    'log_dir': '/code/tmp/logs',
    'errors_dir': '/code/tmp/errors',
    'dataframes_dir': '/code/tmp/dataframes'
}

for dir_name in AUX_DIRS:
    if not os.path.exists(AUX_DIRS[dir_name]):
        os.makedirs(AUX_DIRS[dir_name])

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'postgres',
         'USER': 'postgres',
         'HOST': 'db',
         'PORT': 5432,
     }
}

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

ERROR_HANDLER = ['DBErrorHandler', 'SlackErrorHandler']

TIME_ZONE = 'Europe/Madrid'
