from django.conf.urls.defaults import *
from sys import path
import os.path

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
LANGUAGE_CODE = 'en'

SITE_ID = 1 # ID of the site, used in table names etc
SITE_KEY = 'localhost' # domain of the site, used in creation of full URLs to your site
SITE_DOMAIN = 'http://localhost:8080' # Domain URL used for creating full links in RSS etc.
SITE_NAME = 'Diamanda' # name displayed in templates
SITE_DESCRIPTION = 'Diamanda' # description of the site used in meta description
SITE_ADMIN_MAIL = '2@2.pl' # email shown to the users in User Panel as a contact mail
NOTIFY_ADMINS = False # if true add topic/post will send a email to admin
FORUM_MAX_ANONYMOUS_POSTS_PER_HOUR = 10 # how many posts may be made by anonymous within an hour from now
FORUM_MAX_USER_POST_PER_HOUR = 10 # how many posts may be made by every logged in user within an hour from now. 0 - no limit
GOOGLE_AJAX_SEARCH_API_KEY = '' # required for searching your site with Google :)

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'site_media')
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
    'pagestats.statsMiddleware.statsMiddleware',
    'django_openidconsumer.middleware.OpenIDMiddleware',
    'userpanel.userMiddleware.userMiddleware',
    #'profiler.ProfileMiddleware', # debug !
    #'profiler_sql.SQLLogMiddleware', # debug !
)

AUTHENTICATION_BACKENDS = (
    'userpanel.openIdAuth.OpenIdBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"bib.bib",)

ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
'diamandas/myghtyboard/templates',
'diamandas/userpanel/templates',
'diamandas/pagestats/templates',
'diamandas/pages/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.admin',
    'django_openidconsumer',
    'pagestats',
    'pages',
    'userpanel',
    'myghtyboard',
    )
