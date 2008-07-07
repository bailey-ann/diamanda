from django.conf.urls.defaults import *

# Wiki* URLs
urlpatterns = patterns('diamandas.pagestats',
(r'^/?$', 'views.mainpage'),
(r'^entries/$', 'views.entries'),
(r'^refs/$', 'views.referers'),
(r'^google/$', 'views.google'),
(r'^delete/$', 'views.delete_all'),
)
