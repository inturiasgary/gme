# -*- coding: utf-8 -*-
import os

DIR_ACTUAL = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gary Inturias Rojas', 'inturiasgary@hotmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    
DATABASE_NAME = 'database.db'  
DATABASE_USER = ''             
DATABASE_PASSWORD = ''         
DATABASE_HOST = ''             
DATABASE_PORT = ''             

TIME_ZONE = 'America/La_Paz'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'site_media/')
MEDIA_URL = '/site_media/'

ADMIN_MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'admin_media/')
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qqxw-529(6@57su-f+#lh63kwif9r(&d0m!paa48yv7-n@18y5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cuenta.middleware.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware', #para la paginacion
    
)

ROOT_URLCONF = 'gme.urls'

TEMPLATE_DIRS = (
    os.path.join(DIR_ACTUAL,'templates'),
    
)

TEMPLATE_CONTEXT_PROCESSORS =(
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "cuenta.context_processors.cuenta",
    "misc.context_processors.contact_email", #para que utilizern los email
    "misc.context_processors.site_name",
    
    "notification.context_processors.notification",
)

INSTALLED_APPS = (
    'django.contrib.auth', #adicionado para el control de autentificacion
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    
    #aplicaciones secundarias a django
    'notification',     #adicionado app externa notification para notificaciones en tiempo r
    'microblog',        #adicionado app microblog
    'repositorio',      #adicionado app repositorio
    'cuenta',           #adicionado app cuenta, administrador de cuentas
    'about',
    'misc',
    'ajax_validation',
    'emailconfirmation',
    'perfiles',         #adicionado app perfiles, administrador de perfiles de usuario
    'pagination',#adicionado app para la paginacion
    'todo',
)

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/microblog/u/%s/" % o.username,
}

AUTH_PROFILE_MODULE = 'perfiles.Perfil' #configuracion para los perfiles de usuario
NOTIFICATION_LANGUAGE_MODULE = 'cuenta.Cuenta'

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
CONTACT_EMAIL = "inturiasgary@gmail.com"
SITE_NAME = "Gme"
LOGIN_URL = "/cuenta/login"
LOGIN_REDIRECT_URLNAME = "what_next"

#configuracion para email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'inturiasgary@gmail.com'
EMAIL_HOST_PASSWORD = 'iomegasys123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#LANGUAGES
LANGUAGES = (('en-us',u'English'),('es-es',u'Español'))
