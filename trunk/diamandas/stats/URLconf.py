from django.conf.urls.defaults import *

# Wiki* URLs
urlpatterns = patterns('stats',
(r'^entries/$', 'views.entries'),
(r'^refs/$', 'views.referers'),
(r'^google/$', 'views.google'),
(r'^delete/$', 'views.delete_all'),
)
