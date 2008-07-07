from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('diamandas.pages.views',
(r'^$', 'show_help'),
(r'^p/(?P<slug>[\w\-_]+)/', 'show'),
(r'^submit/r/(?P<sid>[0-9]+)/', 'show_submission'),
(r'^submit/', 'submit_content'),
(r'^mdk/', 'preview'),
(r'^rss/$', 'full_rss'),
(r'^r/(?P<slug>[\w\-_]+)/', 'book_rss'),
(r'^search/$', 'search_pages'),
(r'^n/$', 'list_news'),
(r'^n/(?P<book>[\w\-_]+)/$', 'list_news'),
)
