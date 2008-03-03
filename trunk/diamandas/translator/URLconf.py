from django.conf.urls.defaults import *

urlpatterns = patterns('translator',
(r'^show/(?P<tid>(\d+))/$', 'views.tra_show'),
(r'^apply/(?P<tid>(\d+))/$', 'views.tra_apply'),
(r'^get_po/(?P<tid>(\d+))/$', 'views.get_po'),
(r'^list/$', 'views.tra_list'),
(r'^$', 'views.translations'),
)
