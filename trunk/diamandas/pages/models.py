#!/usr/bin/python
# Diamanda Application Set
# Pages module
from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from boxcomments.models import Comment
from cbcplugins import cbcparser

class Content(models.Model):
	"""
	main Content model
	"""
	CONTENT_TYPE = (('news', _('News')), ('page', _('Article')), ('book', _('Book')))
	
	title = models.CharField(max_length=255, verbose_name=_('Title'))
	slug = models.SlugField(max_length=255, unique=True, prepopulate_from=("title", ), verbose_name=_('Slug'))
	description = models.TextField(verbose_name=_('Description'))
	parsed_description = models.TextField(verbose_name=_('Description'), blank=True)
	text = models.TextField(verbose_name=_('Text'), blank=True)
	parsed_text = models.TextField(verbose_name=_('Text'), blank=True)
	content_type = models.CharField(max_length=255, verbose_name=_('Type'), choices=CONTENT_TYPE)
	place = models.ForeignKey('self', verbose_name=_('Place in'), blank=True, null=True, limit_choices_to={'content_type': 'book'})
	date = models.DateTimeField(blank=True, null=True)
	is_update = models.BooleanField(blank=True, default=False, verbose_name=_('Updated'))
	is_markup = models.BooleanField(blank=True, default=True, verbose_name=_('Using markdown'))
	changes = models.CharField(max_length=255, verbose_name=_('Changes summary'), blank=True)
	book_order = models.PositiveSmallIntegerField(default=0, verbose_name=_('Book order'), blank=True, help_text=_('If you add a book and want to display a link to it in the menu enter 1 or greater value'))
	
	comments_count = models.PositiveIntegerField(default=0, blank=True)
	current_book = models.CharField(max_length=255, blank=True)
	current_book_title = models.CharField(max_length=255, blank=True)
	crumb = models.CharField(max_length=255, blank=True)
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
			'fields': ('title', 'slug', 'description', 'text', 'content_type','place', 'book_order', 'is_markup', 'is_update', 'changes')
			}),
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
		self.update_entry()

	def update_entry(self):
		"""
		Parse markup, gather other data
		"""
		if self.is_markup:
			self.parsed_description = cbcparser.parse_cbc_tags(self.description)
			self.parsed_text = cbcparser.parse_cbc_tags(self.text)
		else:
			self.parsed_description = self.description
			self.parsed_text = self.text
		
		self.comments_count = Comment.objects.filter(apptype= 1, appid = self.id).count()
		
		crumb = '<a href="/w/p/%s/">%s</a>' % (self.slug, self.title)
		a = self
		if a.place:
			while a:
				crumb = '<a href="/w/p/' + a.place.slug + '/">' + a.place.title + '</a> > ' + crumb
				a = a.place
				if not a.place:
					a = False
			
		self.crumb = crumb
		
		if self.content_type == 'book':
			self.current_book = self.slug
			self.current_book_title = self.title
		elif self.place.content_type == 'book':
			self.current_book = self.place.slug
			self.current_book_title = self.place.title
		else:
			self.current_book = False
			self.current_book_title = False
		super(Content, self).save()

