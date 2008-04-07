Diamanda Applications Set 2008.04 Test 1
Author: Piotr Maliński ("Riklaunim")
Mail: riklaunim@gmail.com
License: GPL



~~ Components ~~
Currently Diamanda has several apps: 
* Content (diamandas/pages)
* Forum MyghtyBoard (diamandas/myghtyboard)
* Stats (diamandas/stats)
* User Panel (diamandas/userpanel)
* Global Comments (diamandas/boxcomments)
* Gettext Translation Manager (diamandas/translator)
* ContentBBCode Tag system (diamandas/cbcplugins, not a Django application)


~~ Dependencies ~~
Here is a list of extra python modules that Diamanda uses: 
* Django-SVN (tested on 0.97-pre-SVN-7403)
* PIL - User Panel, ContentBBCode
* strip-o-gram - most of applications
* Pygments - ContentBBCode and MyghtyBoard (FBC template tag)
* polib - Gettext Translation Manager


~~ How to start the dev server ~~
* Check settings.py (SQLite by default)
* Create tables and superuser (If the SQLite database file already exists - delete it): 
    python manage.py syncdb
    python manage.py runserver 8080

