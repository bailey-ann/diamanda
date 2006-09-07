from django.conf.urls.defaults import *
from wiki.feeds import *
# feeds for wikiPages and wikiNews
feeds = {
    'latestpages': LatestPages,
    'latestnews': LatestNews,
    'latestnewsbycategory': LatestNewsByCategory,
}

sitemaps = {
	'wiki': Wiki,
	}

urlpatterns = patterns('',
(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': '/home/piotr/svn/diamanda/media'}), # change it or remove if not on dev server
(r'^admin/', include('django.contrib.admin.urls')), # admin panel
(r'^forum/', include('myghtyboard.URLconf')), # forum
(r'^/?$', 'wiki.views.show_page'), # wiki main page under /
(r'^wiki/', include('wiki.URLconf')), # wiki
(r'^wiki/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}), # wiki feeds
(r'^wiki/sitemap.xml$', 'django.contrib.sitemap.views.sitemap', {'sitemaps': sitemaps}), # wikiPages sitemap
)
