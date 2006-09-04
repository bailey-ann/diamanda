from wiki.models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.syndication.feeds import Feed
from django.contrib.sitemap import Sitemap
from django.conf import settings

class LatestPages(Feed):
	title = settings.SITE_NAME
	link = settings.SITE_NEWS_LINK 
	description = settings.SITE_DESCRIPTION
	def items(self):
		return Page.objects.order_by('-creation_date')[:10]

class LatestNews(Feed):
	title = settings.SITE_NAME
	link = settings.SITE_NEWS_LINK 
	description = settings.SITE_DESCRIPTION
	def item_link(self):
		return ''
	def items(self):
		return News.objects.order_by('-news_date')[:10]

class LatestNewsByCategory(Feed):
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		return bits[0]
	title = settings.SITE_NAME
	link = settings.SITE_NEWS_LINK 
	description = settings.SITE_DESCRIPTION
	def item_link(self):
		return ''
	def items(self, obj):
		category = Category.objects.get(id=obj)
		return category.news_set.all().order_by('-news_date')[:10]

class Wiki(Sitemap):
	def items( self ):
		return Page.objects.order_by('-creation_date')
	def lastmod( self, obj ):
		return obj.modification_date
	def changefreq(self, obj):
		return 'monthly'
	def priority(self, obj):
		if obj.slug == 'index':
			return '1.0'
		else:
			return '0.5'
		