from pathlib import Path
import os
import environ
import dj_database_url

SITE_ID = 1

env = environ.Env(DEBUG=(bool, False))


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [ 
    'saaco.onrender.com',
    '127.0.0.1',
    'localhost',
    'saacoapp.com'
]


CORS_ALLOWED_ORIGINS = [
    "https://saacoapp.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.saacoapp\.com$",
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

# Application definition
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'app',
    'api',
    # Installed app
    "corsheaders",
    # GOOGLE AUTH
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
          'profile',
          'email'
        ],
        'AUTH_PARAMS': { "access_type": "online"}
        ,
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_SECRET_KEY'),
            'key': ''
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Cor Middlware
    "corsheaders.middleware.CorsMiddleware",
    # End
    "django.middleware.common.CommonMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ALL AUTH    
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'saaco.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
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

WSGI_APPLICATION = 'saaco.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if not DEBUG:# Replace the SQLite DATABASES configuration with PostgreSQL:
    DATABASES = {
        'default': dj_database_url.config(        # Replace this value with your local database's connection string.        
                default=env(DATABASE_URL_EXTERNAL),
                conn_max_age=600
            )
        }

# if DEBUG:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_REDIRECT_URL = "/home/"
LOGOUT_REDIRECT_URL = "/user/login/" 

# STATIC_ROOT = BASE_DIR / 'static/'
# files storage during development
# STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [  os.path.join(BASE_DIR, "static"),
# ]


# if  DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static/']
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'
# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR,'media')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
