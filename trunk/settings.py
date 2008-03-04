DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    #('', ''),
)

MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'diamandadb'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'

SITE_ID = 1
SITE_KEY = 'localhost:8080'

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"bib.bib",)


from sys import path
path.append('diamandas/')

SITE_NAME = 'Diamanda'
SITE_DESCRIPTION = 'Diamanda'
VALID_TAGS = ('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote')
GOOGLE_AJAX_SEARCH_API_KEY = ''

MEDIA_ROOT = '/home/piotr/biblioteka/site_media/'
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '2tv6q=sq%k1d34t1i#8me%y(og71s##h1m57h7$g)_q2$p^#xc'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'stats.statsMiddleware.statsMiddleware',
    'userpanel.userMiddleware.userMiddleware',
)

ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
'diamandas/myghtyboard/templates',
'diamandas/userpanel/templates',
'diamandas/stats/templates',
'diamandas/pages/templates',
'diamandas/polls/templates',
'diamandas/translator/templates',
'diamandas/boxcomments/templates'
'diamandas/gcodesearch/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'stats',
    'pages',
    'polls',
    'boxcomments',
    'userpanel',
    'myghtyboard',
    'translator',
    'gcodesearch',
)
