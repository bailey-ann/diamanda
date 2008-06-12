#!/usr/bin/python
# Diamanda Application Set
# Pages module
from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from cbcplugins import cbcparser
from myghtyboard.models import Topic, Forum
from pages.feedupdate import *

class Content(models.Model):
	"""
	main Content model
	"""
	CONTENT_TYPE = (('news', _('News')), ('page', _('Article')), ('book', _('Book')))
	ORDER_HELP = _('If you add a book and want to display a link to it in the menu enter 1 or greater value')
	CFORUM = _('Select a forum in which comment topics will be created (for this and child entries). You can set this for every book, and Articles/News placed in them will use book settings.')
	
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
	is_markup = models.BooleanField(blank=True, default=True, verbose_name=_('Using markdown'), help_text=_('If checked markdown parser will be run on text and description.'))
	changes = models.CharField(max_length=255, verbose_name=_('Changes summary'), blank=True)
	book_order = models.PositiveSmallIntegerField(default=0, verbose_name=_('Book order'), blank=True, help_text=ORDER_HELP)
	author = models.ForeignKey(User, verbose_name=_('Author'))
	
	comments_count = models.PositiveIntegerField(default=0, blank=True)
	coment_topic = models.ForeignKey(Topic, blank=True, null=True)
	coment_forum = models.ForeignKey(Forum, blank=True, null=True, help_text=CFORUM)
	current_book = models.CharField(max_length=255, blank=True)
	current_book_title = models.CharField(max_length=255, blank=True)
	crumb = models.CharField(max_length=255, blank=True)
	class Meta:
		verbose_name = _('Content')
		verbose_name_plural = _('1. Content')
		db_table = 'rk_content' + str(settings.SITE_ID)
	class Admin:
		list_display = ('title', 'slug', 'content_type', 'place')
		list_filter = ['date', 'content_type']
		search_fields = ['title', 'slug', 'text']
		fields = (
		(_('Content'), 
			{
			'fields': ('title', 'slug', 'description', 'text', 'content_type','place', 'author', 'is_markup')
			}),
		(_('Book'), 
			{
			'fields': ('book_order', 'coment_forum')
			}),
		(_('Updates'), 
			{
			'fields': ('is_update', 'changes')
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
			self.parsed_description = cbcparser.parse_cbc_tags(self.description, False)
			self.parsed_text = cbcparser.parse_cbc_tags(self.text, False)
		
		self.comments_count = 0 # TUTAJ Z FORUM !!
		
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
		elif self.place and self.place.content_type == 'book':
			self.current_book = self.place.slug
			self.current_book_title = self.place.title
		else:
			self.current_book = False
			self.current_book_title = False
		super(Content, self).save()
		make_feed(settings.SITE_ID)


class Attachment(models.Model):
	"""
	Support for Content attachments / multisite
	"""
	TYPES = [('image', _('Image')), ('other', _('Other'))]
	file = models.CharField(max_length=255, verbose_name=_('File'))
	filetype = models.CharField(max_length=255, verbose_name=_('Type'), choices=TYPES)
	site = models.CharField(max_length=255, verbose_name=_('Site'), blank=True, default=settings.SITE_KEY)
	page = models.ForeignKey(Content, verbose_name=_('Page'))
	author = models.ForeignKey(User, verbose_name=_('Author'))
	class Meta:
		verbose_name = _('Attachment')
		verbose_name_plural = _('Attachments')
	class Admin:
		list_display = ('file', 'filetype', 'site', 'page', 'author')
		list_filter = ['site', 'filetype']
		search_fields = ['file']
	def __str__(self):
		return self.file
	def __unicode__(self):
		return self.file

class Archive(models.Model):
	"""
	archived content entries and edit proposals
	"""
	page = models.ForeignKey(Content, verbose_name=_('Source Page'))
	description = models.TextField(verbose_name=_('Description'))
	text = models.TextField(verbose_name=_('Text'), blank=True)
	date = models.DateTimeField(blank=True, null=True)
	changes = models.CharField(max_length=255, verbose_name=_('Changes summary'), blank=True)
	author = models.ForeignKey(User, verbose_name=_('Author'))
	is_proposal = models.BooleanField(blank=True, default=True, verbose_name=_('Proposal'))
	class Meta:
		verbose_name = _('Archive')
		verbose_name_plural = _('Archive')
		db_table = 'rk_archive' + str(settings.SITE_ID)
	class Admin:
		list_display = ('page', 'author', 'date', 'changes')
		list_filter = ['date', 'author', 'page']
		fields = (
		(None, 
			{
			'fields': ('page', 'description', 'text', 'date', 'changes','author')
			}),
		)
	def __str__(self):
		return self.page
	def __unicode__(self):
		return self.page

class Feed(models.Model):
	"""
	storage for "what's new?" feeds
	"""
	site = models.PositiveSmallIntegerField(verbose_name=_('Site ID'), unique=True)
	text = models.TextField(verbose_name=_('Feed content'))
