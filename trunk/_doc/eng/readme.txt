Diamanda Applications Set 2008.07 Test 3
Author: Piotr Maliński ("Riklaunim")
Mail: riklaunim@gmail.com
License: GPL


DIAMANDA 2008.07 Test 3 IS NOT COMPATIBLE WITH NEWFORMS-ADMIN
TESTED with Django-SVN revision 7952

~~ Components ~~
Currently Diamanda has several apps: 
* Content (diamandas/pages)
* Forum MyghtyBoard (diamandas/myghtyboard)
* Stats (diamandas/stats)
* User Panel (diamandas/userpanel)
* ContentBBCode Tag system (diamandas/cbcplugins, not a Django application)
Applications removed from Diamanda 2007 will be available in Diamanda Extras.

~~ Dependencies ~~
Here is a list of extra python modules that Diamanda uses: 
* Django-SVN (tested on 0.97-pre-SVN-7403)
* PIL - ContentBBCode
* Pygments - ContentBBCode and MyghtyBoard
* Python-OpenID (+yadis +elementree)


~~ How to start the dev server / Diamanda 2007 ~~
* Check settings.py (SQLite by default)
* Create tables and superuser (If the SQLite database file already exists - delete it): 
    python manage.py syncdb
    python manage.py runserver 8080

~~ HELP ~~
* English: www.rkblog.rk.edu.pl / riklaunim@gmail.com (mail/jabber)
* Polish: www.python.rk.edu.pl
