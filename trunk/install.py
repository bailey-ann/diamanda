from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from wiki.models import *
from myghtyboard.models import *


Page.objects.all().delete()
p = Page(title='Diamanda Wiki Main Page', slug='index', description='A description :)', text='''[rk:h id="1"]Diamanda Wiki SVN[/rk:h]
[toc]<br /><br />

Diamanda (wiki, forum and other apps) is released under GPL License<br />
<b>Author</b>: Piotr Malinski - riklaunim@gmail.com | <a href="http://www.rkblog.rk.edu.pl">English support</a> | <a href="http://www.python.rk.edu.pl">Polskie Wsparcie</a><br />

<div class="box">This applications is in developement and currently is in Quasi-Stable stage.</div>
<br />
[rk:h id="2"]Features[/rk:h]
<b>WIKI</b>
<blockquote>
- add, Edit Pages with permission controll<br />
- full history support<br />
- diffs between all versions of a wikiPage<br />
- safe HTML markup and plugable ContentBBcode tags<br />
- google sitemap generation<br />
</blockquote><br />
<b>MyghtyBoard Forum</b>
<blockquote>
- Add Topic/Post<br />
- Edit my posts<br />
- Permission controll, user cant post a new post after his post<br />
- IP saved<br />
- Lock/Open topics, sticky/global topics<br />
- Topics with my posts, My Topics, Last active Topics lists<br />
- Move Topics
</blockquote>
<b>OTHER APPS</b>
<blockquote>
- Task Manager: manage site tasks and helps coordinate users work<br />
- News: simple news system with keywords<br />
- User Panel: User Profile, users list, sending messages (emails), login and register with Captcha<br />
- Site Statistics (under /stats/ for admins): unique entries, referers, keywords from google
</blockquote>

<div class="box"><b>NOTE!</b><br />
- All applications can be rather easily used alone (requires some small changes) See support sites for more details.</div><br />

[rk:h id="2"]Requirements:[/rk:h]
- install <b>strip-o-gram</b> from <a href="http://www.zope.org/Members/chrisw/StripOGram" target="_blank">here</a> - its a safe HTML filter which is used in Diamanda WikiPages and forums.
<div class="box">python setup.py install</div>
will install it.<br />
- <b>pygments</b>: for code highlighting.<br />
- <b>PIL - Python Imaging Library</b>: makes thumbs and Captcha<br /><br />

[rk:h id="2"]Instalation:[/rk:h]
- edit urls.py and change the site_media path /home/piotr/diamanda/media to that on your computer:
<div class="box">(r^site_media/(.*)$, django.views.static.serve, {document_root: /path/here}),</div>

- create tables (sqlite3 by default):
<div class="box">python manage.py syncdb<br />
python install.py</div>
- create a superuser when creating tables!<br />

- run the dev server: 
<div class="box">python manage.py runserver 8080</div>
<br />

<div class="box">Debug is set to True by default!</div>
<br /><br />

[rk:h id="2"]MyghtyBoard[/rk:h]
MyghtyBoard is the name of the forum script  - it doesn't require myghty (the template framework) but in very old times "MyghtyBoard" was a mygty based forum skeleton app ;) so I've kept the name.<br />
Categories and Forums are managed by the Django Admin Panel. Staff members and superusers are forum moderators.
<br /><br />

[rk:h id="2"]Extra settings in settings.py[/rk:h]
There is some extra settings variables in <b>settings.py</b>.<br />
- RSS settings are used when generating RSS Feeds.<br />
- Anonymous Permissions: True/False<br /><br />

[rk:h id="2"]Logged in users - Permissions[/rk:h]
- add, edit perms are used on Wiki Pages to check if user can add or edit pages. Extra permission:<br />
"Can set Page as current" - can set edited page as current<br /><br />

[rk:h id="3"]CAN_SET_CURENT and Edit Proposals[/rk:h]
If someone cant set edited page as current it will be saved as a one of older versions of that Wiki Page but it will be market as Edit Proposal 
and on the history list will be highlighted in green. Staff members can "unpropose" it (becomes normal "old version") or anyone who CAN_SET_CURENT and edit can
restore it / and if needed - edit it.<br />
- A list of all Edit Proposals can be found on /wiki/proposals/<br /><br />

[rk:h id="2"]RSS Feeds[/rk:h]
<div class="box">http://localhost:8080/rss/latestpages/ - latest pages<br />
http://localhost:8080/rss/latestnews/ - latest pages</div>
<br />

[rk:h id="2"]Sitemap[/rk:h]
<div class="box">http://localhost:8080/sitemap.xml</div>
<br />

[rk:h id="2"]ContentBBCode[/rk:h]
Wiki CBC Descriptions module in the Admin Panel is designed to keep descriptions of all CBC plugins you have. ContentBBcode is a pluggable 
tags system (CBC for short). A CBC plugin can be a JS widget wrapper or perform other dynamic operations like display latest changes on the wiki.
''', changes='Page Creation', creation_date='2006-09-04 15:42:46', modification_date='2006-09-04 15:42:46', modification_user='piotr', modification_ip='666.69.69.69')
p.save()

from django.contrib.auth.models import Group, Permission
Group.objects.all().delete()
g = Group(name='users')
g.save()
g.permissions.add(Permission.objects.get(codename='can_set_current'), Permission.objects.get(codename='add_page'), Permission.objects.get(codename='add_taskcomment'), Permission.objects.get(codename='change_page'), Permission.objects.get(codename='add_topic'), Permission.objects.get(codename='add_post'))
