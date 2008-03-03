#!/usr/bin/python
# Diamanda Application Set
# Pages module
from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class ForeignCategoryContent(models.ForeignKey):
	"""
	Custom ForeignKey that will show only Content objects with content_type='book'
	"""
	def __init__(self, to, to_field=None, **kwargs):
		models.ForeignKey.__init__(self, to, to_field=None, **kwargs)
	def get_choices(self, include_blank=True):
		c = Content.objects.filter(content_type='book')
		returnList = [('', '---------')]
		for cc in c:
			returnList.append([cc.id, cc.title])
		return returnList

class Content(models.Model):
	"""
	main Content model
	"""
	CONTENT_TYPE = (('news', _('News')), ('page', _('Article')), ('book', _('Book')))
	
	title = models.CharField(max_length=255, verbose_name=_('Title'))
	slug = models.SlugField(max_length=255, unique=True, prepopulate_from=("title", ), verbose_name=_('Slug'))
	description = models.TextField(verbose_name=_('Description'))
	text = models.TextField(verbose_name=_('Text'), blank=True)
	content_type = models.CharField(max_length=255, verbose_name=_('Type'), choices=CONTENT_TYPE)
	place = ForeignCategoryContent('self', verbose_name=_('Place in'), blank=True, null=True)
	date = models.DateTimeField(blank=True, null=True)
	is_update = models.BooleanField(blank=True, default=False)
	wykop = models.CharField(max_length=255, verbose_name='Wykop', blank=True)
	jakilinux = models.CharField(max_length=255, verbose_name='Jakilinux', blank=True)
	digg = models.CharField(max_length=255, verbose_name='Digg', blank=True)
	reddit = models.CharField(max_length=255, verbose_name='Reddit', blank=True)
	changes = models.CharField(max_length=255, verbose_name=_('Changes summary'), blank=True)
	class Meta:
		verbose_name = _('Content')
		verbose_name_plural = _('Content')
		db_table = 'rk_content' + str(settings.SITE_ID)
	class Admin:
		list_display = ('title', 'slug', 'content_type', 'place')
		list_filter = ['date']
		search_fields = ['title', 'slug', 'text']
		fields = (
		(None, 
			{
			'fields': ('title', 'slug', 'description', 'text', 'content_type', 'place')
			}),
		(_('Other'),
			{'fields': ('is_update', 'changes', 'wykop', 'jakilinux', 'digg', 'reddit'), 'classes': 'collapse'}),
		)
	def get_absolute_url(self):
		return '/w/p/' + self.slug + '/'
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title
	def save(self):
		try:
			c = Content.objects.get(id=self.id)
		except:
			self.date = datetime.now()
		else:
			if self.is_update:
				self.date = datetime.now()
			else:
				self.date = c.date
		super(Content, self).save()
