from django.conf.urls.defaults import *
from sys import path

path.append('diamandas/')

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
SITE_KEY = 'localhost'
SITE_NAME = 'Diamanda'
SITE_DESCRIPTION = 'Diamanda'
SITE_ADMIN_MAIL = '2@2.pl'
NOTIFY_ADMINS = True
VALID_TAGS = ('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote')
GOOGLE_AJAX_SEARCH_API_KEY = ''

MEDIA_ROOT = '/home/piotr/svn/diamanda/site_media/'
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'



DEFAULT_HOME_TEXT = '''Diamanda Application Set :) Visit <a href="http://www.rkblog.rk.edu.pl">rkblog.rk.edu.pl</a> for support, docs and more :]<br /><br />
				You can edit this text by editing DEFAULT_HOME_TEXT in settings.py, or just by adding a Content entry with "index" slug.
				<div class="content_box_header">Diamanda resources and help</div>
				<div  class="content_box">
				<ul>
				<li><a href="http://www.rkblog.rk.edu.pl">English Support</a></li>
				<li><a href="http://www.python.rk.edu.pl">Polish Support</a></li>
				<li><a href="http://code.google.com/p/diamanda/">SVN repository at code.google.com</a></li>
				<li><a href="http://code.djangoproject.com/wiki/ForumAppsComparison">Django Forum Apps Comparison</a></li>
				</ul>
				</div>
				<p style="text-align:center; margin-top:5px;">
				<a href="http://validator.w3.org/check?uri=referer"><img
					src="http://www.w3.org/Icons/valid-xhtml10-blue"
					alt="Valid XHTML 1.0 Transitional" height="31" width="88" /></a>
				</p>'''
#################################
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/'
AUTH_PROFILE_MODULE = 'userpanel.profile'
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
    #'profiler.ProfileMiddleware', # debug !
    #'profiler_sql.SQLLogMiddleware', # debug !
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"bib.bib",)

ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
'diamandas/myghtyboard/templates',
'diamandas/userpanel/templates',
'diamandas/stats/templates',
'diamandas/pages/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.admin',
    'stats',
    'pages',
    'userpanel',
    'myghtyboard',
    )
