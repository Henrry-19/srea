from lib2to3.pytree import Base
from pathlib import Path
import os
import environ

env= environ.Env()
environ.Env.read_env()

from core.db.db import MYSQL #Importar la base de datos


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent #Directorio de nuestro proyecto django

#NPM_BIN_PATH = "C:/Users/jimen/AppData/Roaming/npm" #OJO ESO HAY QUE GESTIONAR PARA LA INSTALACIÓN
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #libs
    'widget_tweaks', #Me permite incrustar atributos en mis componentes
    #Apps
    'apps.srea',
    'apps.homepage',
    'apps.login',
    'apps.user'

   

]

######JAZZMIN#######
JAZZMIN_SETTINGS ={
# title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title":'SREA',
# Welcome text on the login screen
    "welcome_sign":'Inicio de sesión',
# Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "../static/img/study.png",
#----------------------------------------------
    'icons':{
        'auth.Group':'fas fa-users',
        'user.user':'fas fa-user',
        'srea.asignatura':'fas fa-book'

    }
}



INTERNAL_IPS = [
    "127.0.0.1",
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware'
    
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')], #Concatenar las dos rutas, rutas que contienen nuestras templates
        'APP_DIRS': True, #Buscar en los templates de nuestras aplicaciones
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
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = MYSQL #Configuración de la base de datos


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

#Trabajando con los archivos estáticos
STATIC_URL = '/static/' #Permite trabajar con la ruta de nuestros archivos estáticos 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static"), #Ruta en la que van a estar alojados mis archivos estáticos
]

#path.join-->permite unificar una ruta

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend', 
]

SITE_ID = 1 
#AUTH_USER_MODEL = 'srea.Usuario' #Como modelo para todo el sistema, utiliza este modelo para la autenticación

LOGIN_REDIRECT_URL ='/srea/index1/'


#LOGOUT_REDIRECT_URL ='/login/'
LOGOUT_REDIRECT_URL ='/login/'

LOGIN_URL = '/login/'
#LOGIN_URL = '/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') #Carpeta raíz, se alojan mis archivos media (imágenes, docuementos) 

MEDIA_URL = '/media/' #Url absoluta para trabajar con estos archivos media 

#Modelo personalizado
AUTH_USER_MODEL = 'user.User'

########Permite trabajar con los objetos dentro de las sesiones###########
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

####Correo electrónico####
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DOMAIN = ''


