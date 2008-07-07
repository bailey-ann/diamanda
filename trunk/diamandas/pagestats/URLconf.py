from django.conf.urls.defaults import *

# Wiki* URLs
urlpatterns = patterns('diamandas.pagestats.views',
(r'^/?$', 'mainpage'),
(r'^entries/$', 'entries'),
(r'^refs/$', 'referers'),
(r'^google/$', 'google'),
(r'^delete/$', 'delete_all'),
)
