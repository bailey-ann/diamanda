from django.shortcuts import render_to_response
from news.models import *
from django.conf import settings


# list tasks
def news_by_keywords(request, k_id, pagination_id = 1):
	from django.views.generic.list_detail import object_list
	k = Keywords.objects.get(id=k_id).news_set.all().order_by('-id')
	return object_list(request, k, paginate_by = 10, page = pagination_id, extra_context = {'theme': settings.THEME, 'engine': settings.ENGINE, 'k_id': k_id, 'site_name':settings.SITE_NAME, 'img_path':settings.SITE_IMAGES_SRC_PATH}, template_name = 'news/' + settings.ENGINE + '/knews_list.html')


