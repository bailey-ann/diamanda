from django.conf.urls.defaults import *
import django.contrib.auth.views

urlpatterns = patterns('diamandas.userpanel.views',
(r'^$', 'user_panel'),
(r'^register/$', 'register'),
(r'^register_openid/$', 'register_from_openid'),
(r'^assign_openid/$', 'assign_openid'),
(r'^login/$', 'login_user'),
(r'^logout/$', 'logout_then_login'),
(r'^delopenid/(?P<oid>[0-9]+)/$', 'remove_openid'),
)

