from django.conf.urls.defaults import *
from news.models import *
from django.conf import settings

urlpatterns = patterns('',
(r'^/?$', 'django.views.generic.list_detail.object_list', {'queryset':News.objects.all().order_by('-id'), 'paginate_by':5, 'allow_empty':True, 'template_name':'news/news_list.html', 'extra_context':{'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID}}),
(r'^/(?P<page>[0-9]+)$', 'django.views.generic.list_detail.object_list', {'queryset':News.objects.all().order_by('-id'), 'paginate_by':5, 'allow_empty':True, 'template_name':'news/news_list.html', 'extra_context':{'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID}}),
(r'^more/(?P<slug>[\w\-_]+)/', 'django.views.generic.list_detail.object_detail', {'queryset':News.objects.all() , 'template_name':'news/news_show.html',  'slug_field':'news_slug', 'extra_context':{'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID}}),
)