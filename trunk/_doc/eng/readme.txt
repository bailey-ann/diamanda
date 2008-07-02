Diamanda Applications Set 2008.07 Test 2
Author: Piotr Maliński ("Riklaunim")
Mail: riklaunim@gmail.com
License: GPL



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


~~ How to start the dev server / Diamanda 2007 ~~
* Check settings.py (SQLite by default)
* Create tables and superuser (If the SQLite database file already exists - delete it): 
    python manage.py syncdb
    python manage.py runserver 8080

