import os

DIR_ACTUAL = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gary Inturias Rojas', 'inturiasgary@hotmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'database.db'  # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/La_Paz'

LANGUAGE_CODE = 'es-bo'

SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__),"site_media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

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
    'cuenta.middleware.LocaleMiddleware', #posiblemente borrar
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
    #'gme.app_plugins',     #adicioanado app app_plugins para la extension de template
    'timezones',        #adicionado app timezones para personalizar zonas horarias
    #'gme.friends',
    'pagination',       #adicionado app para la paginacion
)

#ABSOLUTE_URL_OVERRIDES = {
    #"auth.user": lambda o: "/perfiles/%s/" % o.username,
#}

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

#LOGGING_OUTPUT_ENABLED = False
#LOGGING_SHOW_METRICS = False
#LOGGING_LOG_SQL = False

#INTERNAL_IPS = (
#'127.0.0.1',
#)

#configuracion para email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'inturiasgary@gmail.com'
EMAIL_HOST_PASSWORD = 'iomegasys123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True