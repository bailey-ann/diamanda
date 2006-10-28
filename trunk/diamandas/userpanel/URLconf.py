from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('userpanel',
(r'^$', 'views.user_panel'),
(r'^edit_profile/$', 'views.edit_profile'),
(r'^show_profile/(?P<show_user>.*)/$', 'views.show_profile'),
(r'^pmessage/(?P<target_user>.*)/$', 'views.send_pmessage'),
(r'^login/$', 'views.loginlogout'),
(r'^register/$', 'views.register'),
(r'^userlist/$', 'views.userlist'),
)
