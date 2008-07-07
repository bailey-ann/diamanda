from django.conf.urls.defaults import *

urlpatterns = patterns('diamandas.userpanel.views',
(r'^$', 'user_panel'),
(r'^register/$', 'register'),
(r'^register_openid/$', 'register_from_openid'),
(r'^assign_openid/$', 'assign_openid'),
(r'^login/$', 'login_user'),
(r'^logout/$', 'logout_then_login'),
(r'^password_change/$', 'password_change'),
(r'^password_change/done/$', 'password_change_done'),
(r'^password_reset/$', 'password_reset'),
(r'^password_reset/done/$', 'password_reset_done'),
(r'^delopenid/(?P<oid>[0-9]+)/$', 'remove_openid'),
)
