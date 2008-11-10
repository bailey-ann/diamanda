#!/usr/bin/python
# Diamanda Application Set
# Pages module
from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from diamandas.cbcplugins import cbcparser
from diamandas.myghtyboard.models import Topic, Forum
from diamandas.pages.feedupdate import *

class Content(models.Model):
	"""
	main Content model
	"""
	CONTENT_TYPE = (('news', _('News')), ('page', _('Article')), ('book', _('Book')))
	ORDER_HELP = _('If you add a book and want to display a link to it in the menu enter 1 or greater value')
	CFORUM = _('Select a forum in which comment topics will be created (for this and child entries). You can set this for every book, and Articles/News placed in them will use book settings.')
	CBC = _('You can use Content BBCode tags that can highlight code, or show images with thumbs. See Diamanda online documentation.')
	LEFTMENU = _('You can add links or other content that will be displayer in the side menu. Use <b>div class="panel"</b> to wrap it in a box.')
	
	title = models.CharField(max_length=255, verbose_name=_('Title'))
	slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))
	description = models.TextField(verbose_name=_('Description'), help_text=CBC)
	text = models.TextField(verbose_name=_('Text'), blank=True, help_text=CBC)
	content_type = models.CharField(max_length=255, verbose_name=_('Type'), choices=CONTENT_TYPE)
	place = models.ForeignKey('self', verbose_name=_('Place in'), blank=True, null=True, limit_choices_to={'content_type': 'book'})
	date = models.DateTimeField(blank=True, null=True)
	is_update = models.BooleanField(blank=True, default=False, verbose_name=_('Updated'))
	changes = models.CharField(max_length=255, verbose_name=_('Changes summary'), blank=True)
	book_order = models.PositiveSmallIntegerField(default=0, verbose_name=_('Book order'), blank=True, help_text=ORDER_HELP)
	author = models.ForeignKey(User, verbose_name=_('Author'))
	leftmenu = models.TextField(verbose_name=_('Side Menu'), blank=True, help_text = '%s %s' % (LEFTMENU, CBC))
	
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
		Gather other data, update Feed
		"""
		if self.coment_topic:
			self.comments_count = self.coment_topic.posts
		else:
			self.comments_count = 0
		
		crumb = '<a href="/w/p/%s/">%s</a>' % (self.slug, self.title)
		a = self
		if a.place:
			while a:
				crumb = '<a href="/w/p/' + a.place.slug + '/">' + a.place.title + '</a> &gt; ' + crumb
				a = a.place
				if not a.place:
					a = False
			
		self.crumb = crumb
		
		if self.content_type == 'book' and self.book_order > 0:
			self.current_book = self.slug
			self.current_book_title = self.title
		elif self.place and self.place.content_type == 'book':
			self.current_book = self.place.slug
			self.current_book_title = self.place.title
		else:
			self.current_book = False
			self.current_book_title = False
		super(Content, self).save()
		FeedUpdate(settings.SITE_ID)

class Feed(models.Model):
	"""
	storage for "what's new?" feeds
	"""
	site = models.PositiveSmallIntegerField(unique=True) # site id
	html = models.TextField() # rendered html
	rss = models.CharField(max_length=4) # rss