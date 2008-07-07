from django.conf.urls.defaults import *
import os.path

urlpatterns = patterns('',
(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}), # change it or remove if not on dev server
(r'^admin/', include('django.contrib.admin.urls')),
(r'^w/', include('diamandas.pages.URLconf')),
(r'^forum/', include('diamandas.myghtyboard.URLconf')),
(r'^stats/', include('diamandas.pagestats.URLconf')),
(r'^sitemap/$', 'diamandas.pages.views.sitemap'),
(r'^sitemap.xml$', 'diamandas.pages.views.sitemap'),

(r'^user/', include('diamandas.userpanel.URLconf')),
(r'^openid/$', 'diamandas.django_openidconsumer.views.begin'),
(r'^openid/complete/$', 'diamandas.django_openidconsumer.views.complete'),
(r'^openid/signout/$', 'diamandas.django_openidconsumer.views.signout'),

(r'^/?$', 'diamandas.pages.views.show_index'),
)
