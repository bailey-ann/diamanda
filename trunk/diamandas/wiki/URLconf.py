from django.conf.urls.defaults import *

# Wiki* URLs
urlpatterns = patterns('wiki',
(r'^/?$', 'views.show_page'),
(r'^sitelist/$', 'views.index'),
(r'^user/$', 'views.users'),
(r'^register/$', 'views.register'),
(r'^proposals/$', 'views.proposal_list'),
(r'^unpropose/(?P<archive_id>(\d+))/$', 'views.unpropose'),
(r'^add/(?P<slug>[\w\-_]+)/$', 'views.add_page'),
(r'^page/(?P<slug>[\w\-_]+)/$', 'views.show_page'),
(r'^pdf/(?P<slug>[\w\-_]+)/$', 'views.show_page_as_pdf'),
(r'^oldpage/(?P<archive_id>(\d+))/$', 'views.show_old_page'),
(r'^restore/(?P<archive_id>(\d+))/$', 'views.restore_page_from_archive'),
(r'^diff/$', 'views.show_diff'),
(r'^history/(?P<slug>[\w\-_]+)/$', 'views.show_page_history_list'),
(r'^add/$', 'views.add_page'),
(r'^edit/(?P<slug>[\w\-_]+)/$', 'views.edit_page'),
(r'^news/$', 'views.list_news', {'pagination_id': '1'}),
(r'^news/(?P<pagination_id>[0-9]+)/$', 'views.list_news'),
(r'^news/(?P<pagination_id>[0-9]+)/(?P<category_id>[0-9]+)/$', 'views.list_news_from_category'),
)
