Diamanda Wiki SVN 09.09.2006
Released under GPL License
Piotr Malinski - riklaunim@gmail.com

This is a django powered wiki and a forum in developement

Requirements:
- install strip-o-gram from http://www.zope.org/Members/chrisw/StripOGram - it's a safeHTML filter which is used in Diamanda WikiPages :) python setup.py install will install it.

Instalation:
- edit urls.py and change the site_media path '/home/piotr/diamanda/media' to that on your computer:
(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': '/path/here'}),

- create tables (check DB in settings.py) and populate the data:
python manage.py syncdb
python install.py

- create a superuser when creating tables!

- run the dev server: python
manage.py runserver 8080

- http://localhost:8080/ is the main wiki page
- http://localhost:8080/forum/ is the main MyghtyBoard Forum page

[NOTE, Debug is set to True :)]


MyghtyBoard
############################
MyghtyBoard is the name of the forum script which is in heavy developement right now but all the "basic" features
work nicely. Categories and Forums are managed by the Django Admin Panel. Staff members and superusers are forum moderators.


EXTRA SETTINGS in settings.py
#############################
You will find at the end of the file:

# RSS Settings
SITE_NAME = 'Diamanda Wiki !'
SITE_DESCRIPTION = 'A Diamanda Wiki Script'
SITE_NEWS_LINK = '/' # where links of the RSS feeds should point

# Anonymous perms Settings
ANONYMOUS_CAN_EDIT=True
ANONYMOUS_CAN_ADD=True
ANONYMOUS_CAN_VIEW=True
ANONYMOUS_CAN_SET_CURENT=False

# wiki config
WIKI_USE_PDF = False # 'htmldoc' - uses htmldoc , False - no PDF generation
# if set to nonFalse API KEY "search" will allow also "Search this site with google"
# requires pyGoogle, uses current SITE_ID domain name !!! example.com by default, change it to yours!
WIKI_GOOGLE_SEARCH_API = False # set a string with the google search api to enable it

# myghtyboard config
ANONYMOUS_CAN_ADD_TOPIC=True
ANONYMOUS_CAN_ADD_POST=True
MYGHTYBOARD_THEME='aeolus' # theme name, curren "wow" and "aeolus"
MYGHTYBOARD_LANG='english' # language name for i18n graphics (theme must have images for selected language

# thumb CBC
SITE_IMAGES_DIR_PATH = '/home/piotr/diamanda/media/images/'
SITE_IMAGES_SRC_PATH = '/site_media/images/'

# Other
USE_BANS = False # use WIkiBans to prevent baned from add/edit actions
----------
- RSS settings are used when generating RSS Feeds, SITE_NEWS_LINK doesn't require any changes, the rest can be edited.
- Anonymous Permissions: True/False
- USE_BANS - if True the Wiki Ban module (see Admin Panel) will be used to Ban users from add/edit actions (add, edit, restore actions will be disabled for baned users)



Logged in users - Permissions
############################
- add, edit perms are used on Wiki Pages to check if user can add or edit pages. There are also two extra options:
"Can view Page" - can see pages
"Can set Page as current" - can set edited page as current


CAN_SET_CURENT and Edit Proposals
############################
If someone can't set edited page as current it will be saved as a one of older versions of that Wiki Page but it will be market as Edit Proposal
and on the history list will be highlighted in green. Staff members can "unpropose" it (becomes normal "old version") or anyone who CAN_SET_CURENT and edit can
restore it / and if needed - edit it.
- A list of all Edit Proposals can be found on /wiki/proposals/


RSS Feeds
############################
http://localhost:8080/wiki/feeds/latestpages/ - latest pages
http://localhost:8080/wiki/feeds/latestnews/ - 10 latest news
http://localhost:8080/wiki/feeds/latestnewsbycategory/X/ - where X is the category ID - latest 10 news from that category



Wiki Markup
################################
Wiki uses HTML as a markup :) and some helpers. There are tree CSS styles for creating "boxes":
<div class="note">text here</div>
<div class="notice">text here</div>
<div class="box">text here</div>
Screenshot: http://www.fotosik.pl/showFullSize.php?id=37327c455862e363


ContentBBCode
###############################
Wiki CBC Descriptions module in the Admin Panel is designed to keep descriptions of all CBC plugins you have.


TODO
########################
- Files/Images upload/handling on wikiPages - ideas welcomed
- More CBC
- A lot of work in MyghtyBoard...


ToooooooDooooo
########################
- Fulltext search (SoC code)
- Row level permission (SoC, I'll check this later when the wiki will be "finished")