from django.conf.urls.defaults import *

urlpatterns = patterns('',
(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': '/home/piotr/biblioteka/site_media'}), # change it or remove if not on dev server
(r'^admin/', include('django.contrib.admin.urls')),
(r'^w/', include('pages.URLconf')),
(r'^albion/', include('albion.URLconf')),
(r'^forum/', include('myghtyboard.URLconf')),
(r'^user/', include('userpanel.URLconf')),
(r'^stats/', include('stats.URLconf')),
(r'^tra/', include('translator.URLconf')),
(r'^com/', include('boxcomments.URLconf')),
(r'^news/rss/21/', 'pages.views.book_rss', {'slug': 'django'}),
(r'^bgate/', include('baldur.URLconf')),
(r'^sitemap/$', 'pages.views.sitemap'),
(r'^gcodesearch/$', 'gcodesearch.views.search'),
#(r'^p/(?P<pid>[0-9]+)/$', 'polls.views.show_pcomment'),
#(r'^p/', 'polls.views.show_polls'),
(r'^/?$', 'pages.views.show_index'),
)
