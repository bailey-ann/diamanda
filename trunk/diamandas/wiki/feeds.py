from wiki.models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.syndication.feeds import Feed
from django.contrib.sitemaps import Sitemap
from django.conf import settings

class LatestPages(Feed):
	title = settings.SITE_NAME
	link = settings.SITE_NEWS_LINK 
	description = settings.SITE_DESCRIPTION
	def items(self):
		return Page.objects.order_by('-creation_date')[:10]

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
		