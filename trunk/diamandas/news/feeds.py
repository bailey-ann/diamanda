from news.models import *
from django.contrib.syndication.feeds import Feed
from django.conf import settings

class LatestNews(Feed):
	title = settings.SITE_NAME
	link = settings.SITE_NEWS_LINK 
	description = settings.SITE_DESCRIPTION
	def items(self):
		return News.objects.order_by('-id')[:10]
