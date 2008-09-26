from django.conf.urls.defaults import *
import django.contrib.auth.views

urlpatterns = patterns('diamandas.userpanel.views',
(r'^$', 'user_panel'),
(r'^register/$', 'register'),
(r'^register_openid/$', 'register_from_openid'),
(r'^assign_openid/$', 'assign_openid'),
(r'^login/$', 'login_user'),
(r'^logout/$', 'logout_then_login'),
(r'^password_change/$', 'password_change'),
(r'^password_change/done/$', 'password_change_done'),

#(r'^password_reset/$', 'password_reset'),
#(r'^password_reset/done/$', 'password_reset_done'),

#(r'^password_reset/$', 'password_reset'),
#(r'^password_reset/done/$', 'password_reset_done'),
#(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
#(r'^reset/done/$', 'password_reset_complete'),

(r'^delopenid/(?P<oid>[0-9]+)/$', 'remove_openid'),
)

urlpatterns += patterns('',
(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'userpanel/password_reset_form.html', 'email_template_name':'userpanel/password_reset_email.html'}),
(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'userpanel/password_reset_done.html'}),
(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'userpanel/password_reset_confirm.html'}),
(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'userpanel/password_reset_complete.html'}),
)