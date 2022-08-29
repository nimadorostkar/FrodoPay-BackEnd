from pathlib import Path
import os
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g#7&@7tr6-z88vp01(=*y7tr!f4mm%2%a09*+o7#29g%3em+d&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']






'''
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'authentication.mybackend.ModelBackend',
]
'''



AUTH_USER_MODEL = 'authentication.User'



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shortuuid',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'authentication',
    'transactions',
    'fee',
    'advertise',
    'lottery',
    'web',
    'import_export',
    'django_coinpayments',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'django_extensions',
    'fcm_django'
    #'rest_framework_simplejwt.token_blacklist'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")  # ROOT dir for templates



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}





CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8000',]
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000',]
CORS_ORIGIN_ALLOW_ALL = True






AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]



PUSH_NOTIFICATIONS_SETTINGS = {
        "FCM_API_KEY": "f43637258b57affc7acc873d218d2f5ef3f78cc1",
        "GCM_API_KEY": "f43637258b57affc7acc873d218d2f5ef3f78cc1"
}








cred = credentials.Certificate(os.path.join(BASE_DIR, "core/frodopay-f24e4-firebase-adminsdk-c3id1-f43637258b.json"))
firebase_admin.initialize_app(cred)

FCM_DJANGO_SETTINGS = {
  "APP_VERBOSE_NAME": "FCM",
  "FCM_SERVER_KEY": "f43637258b57affc7acc873d218d2f5ef3f78cc1",
  "ONE_DEVICE_PER_USER": False,
  "DELETE_INACTIVE_DEVICES": False,
}








COINPAYMENTS_ADMIN_ENABLED = True
# Insert your API keys here
COINPAYMENTS_API_KEY = 'b5ab7e069860af7711a209cf1aa3343d330b155643f231189477a1731aaa87ad'
COINPAYMENTS_API_SECRET = 'fcF29cad06dd9900980d3b4221ab7d7afdDF26c9B521337295a43cBDcdd7535B'

COINPAYMENTS_IPN_SECRET = '12345678qwertyui'
COINPAYMENTS_MERCHANT_ID = '4eb1ce03dad6446d68460928de1e7171'
# has EOS - overrides choices for 'currency_original' and 'currency_paid' in Payment model
#COINPAYMENTS_ACCEPTED_COINS = ( ('BTC', 'Bitcoin'), ('ETC', 'Ether Classic'), ('ETH', 'Ether') )






REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
       'django_filters.rest_framework.DjangoFilterBackend'
       ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.AllowAny',
        #'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        #'rest_framework.permissions.IsAuthenticated',
       ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}



SITE_ID = 1
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@frodopay.io' #sender's email-id
EMAIL_HOST_PASSWORD = 'Juj97936' #password associated with above email-id










SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=20),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=3),
}






# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
'''
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
'''


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Directory where uploaded media is saved.
MEDIA_URL = '/media/' # Public URL at the browser





# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
