from django.conf.urls.defaults import *
from news.models import *
from django.conf import settings

# Wiki* URLs
urlpatterns = patterns('',
(r'^/?$', 'django.views.generic.list_detail.object_list', {'queryset':News.objects.all().order_by('-id'), 'paginate_by':10, 'allow_empty':True, 'template_name':'news/' + settings.ENGINE + '/news_list.html', 'extra_context':{'theme': settings.THEME, 'engine': settings.ENGINE, 'site_name':settings.SITE_NAME, 'img_path':settings.SITE_IMAGES_SRC_PATH}}),
(r'^/(?P<page>[0-9]+)$', 'django.views.generic.list_detail.object_list', {'queryset':News.objects.all().order_by('-id'), 'paginate_by':10, 'allow_empty':True, 'template_name':'news/' + settings.ENGINE + '/news_list.html', 'extra_context':{'theme': settings.THEME, 'engine': settings.ENGINE, 'site_name':settings.SITE_NAME, 'img_path':settings.SITE_IMAGES_SRC_PATH}}),

(r'^more/(?P<object_id>(\d+))/', 'django.views.generic.list_detail.object_detail', {'queryset':News.objects.all() , 'template_name':'news/' + settings.ENGINE + '/news_show.html', 'extra_context':{'theme': settings.THEME, 'engine': settings.ENGINE, 'site_name':settings.SITE_NAME}}),

(r'^keywords/(?P<page>[0-9]+)/', 'django.views.generic.list_detail.object_list', {'queryset':Keywords.objects.all().order_by('-id'), 'paginate_by':10, 'allow_empty':True, 'template_name':'news/' + settings.ENGINE + '/keywords_list.html', 'extra_context':{'theme': settings.THEME, 'engine': settings.ENGINE, 'site_name':settings.SITE_NAME}}),
(r'^keywords/', 'django.views.generic.list_detail.object_list', {'queryset':Keywords.objects.all().order_by('-id'), 'paginate_by':10, 'allow_empty':True, 'template_name':'news/' + settings.ENGINE + '/keywords_list.html', 'extra_context':{'theme': settings.THEME, 'engine': settings.ENGINE, 'site_name':settings.SITE_NAME}}),

(r'^k/(?P<k_id>(\d+))/(?P<pagination_id>(\d+))/$', 'news.views.news_by_keywords'),
(r'^k/(?P<k_id>(\d+))/$', 'news.views.news_by_keywords'),
)
