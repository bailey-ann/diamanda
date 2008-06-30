from django.conf.urls.defaults import *
import os.path

urlpatterns = patterns('',
(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}), # change it or remove if not on dev server
(r'^admin/', include('django.contrib.admin.urls')),
(r'^w/', include('pages.URLconf')),
(r'^forum/', include('myghtyboard.URLconf')),
(r'^stats/', include('stats.URLconf')),
(r'^sitemap/$', 'pages.views.sitemap'),
(r'^sitemap.xml$', 'pages.views.sitemap'),

(r'^user/', include('userpanel.URLconf')),
(r'^openid/$', 'django_openidconsumer.views.begin'),
(r'^openid/complete/$', 'django_openidconsumer.views.complete'),
(r'^openid/signout/$', 'django_openidconsumer.views.signout'),

(r'^/?$', 'pages.views.show_index'),
)
