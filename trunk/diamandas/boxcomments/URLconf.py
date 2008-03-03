from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('boxcomments',
(r'^(?P<appid>[0-9]+)/(?P<apptype>[0-9]+)/(?P<quoteid>[0-9]+)/', 'views.comments'),
(r'^(?P<appid>[0-9]+)/(?P<apptype>[0-9]+)/', 'views.comments'),
)
