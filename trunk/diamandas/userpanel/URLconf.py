from django.conf.urls.defaults import *

urlpatterns = patterns('userpanel',
(r'^$', 'views.user_panel'),
(r'^register/$', 'views.register'),
(r'^login/$', 'views.login_user'),
(r'^logout/$', 'views.logout_then_login'),
(r'^password_change/$', 'views.password_change'),
(r'^password_change/done/$', 'views.password_change_done'),
(r'^password_reset/$', 'views.password_reset'),
(r'^password_reset/done/$', 'views.password_reset_done'),
)
