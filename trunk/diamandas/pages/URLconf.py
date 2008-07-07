from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('diamandas.pages',
(r'^$', 'views.show_help'),
(r'^p/(?P<slug>[\w\-_]+)/', 'views.show'),
(r'^submit/r/(?P<sid>[0-9]+)/', 'views.show_submission'),
(r'^submit/', 'views.submit_content'),
(r'^mdk/', 'views.preview'),
(r'^rss/$', 'views.full_rss'),
(r'^r/(?P<slug>[\w\-_]+)/', 'views.book_rss'),
(r'^search/$', 'views.search_pages'),
(r'^n/$', 'views.list_news'),
(r'^n/(?P<book>[\w\-_]+)/$', 'views.list_news'),
)
