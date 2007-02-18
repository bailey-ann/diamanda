from django.conf.urls.defaults import *
from wiki.feeds import *
from news.feeds import *
feeds = {
    'latestpages': LatestPages,
    'latestnews': LatestNews,
}

sitemaps = {
	'wiki': Wiki,
	}

urlpatterns = patterns('',
(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': '/home/piotr/svn/diamanda/site_media'}), # change it or remove if not on dev server
(r'^admin/', include('django.contrib.admin.urls')), # admin panel
(r'^forum/', include('myghtyboard.URLconf')), # forum
(r'^/?$', 'wiki.views.show_page'),
(r'^wiki/', include('wiki.URLconf')), # wiki
(r'^news/', include('news.URLconf')), # wiki
(r'^tasks/', include('tasks.URLconf')), # wiki
(r'^stats/', include('stats.URLconf')), # wiki
(r'^user/', include('userpanel.URLconf')), # user profile
(r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}), # wiki feeds
(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}), # wikiPages sitemap
)
