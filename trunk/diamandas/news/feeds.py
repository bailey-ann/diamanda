from news.models import *
from django.contrib.syndication.feeds import Feed
from django.conf import settings

class LatestNews(Feed):
	title = settings.SITE_NAME
	link = settings.SITE_NEWS_LINK 
	description = settings.SITE_DESCRIPTION
	def items(self):
		return News.objects.order_by('-id')[:10]

class LatestNewsByKeyword(Feed):
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		return bits[0]
	title = settings.SITE_NAME
	link = settings.SITE_NEWS_LINK
	description = settings.SITE_DESCRIPTION
	def items(self, obj):
		return Keywords.objects.get(id=obj).news_set.all().order_by('-id')[:10]
