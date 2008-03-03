from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
(r'^$', 'pages.views.show_index'),
(r'^p/(?P<slug>[\w\-_]+)/', 'pages.views.show'),
(r'^autor/$', 'pages.views.autor'),
(r'^rss/$', 'pages.views.full_rss'),
(r'^r/(?P<slug>[\w\-_]+)/', 'pages.views.book_rss'),
(r'^biblioteki/$', 'pages.views.biblioteki'),
(r'^search/$', 'pages.views.search_pages'),
(r'^n/$', 'pages.views.list_news'),
(r'^n/(?P<book>[\w\-_]+)/$', 'pages.views.list_news'),
)
