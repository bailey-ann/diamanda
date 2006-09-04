from django.db import models
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.conf import settings

# Wiki Categories used for Wiki Pages and Wiki News
class WikiCategory(models.Model):
	DEPTH = (
	('0', '0'),
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),
	('6', '6'),
	('7', '7'),
	('8', '8'),
	('9', '9'),
	('10', '10'),
	)
	objects = CurrentSiteManager()
	site = models.ForeignKey(Site, blank = True, default=settings.SITE_ID)
	cat_parent = models.ForeignKey('self', blank=True, null=True, verbose_name="Parent Category") # parent category if any
	cat_name = models.CharField(maxlength=255, verbose_name="Category Name", unique=True, db_index=True) # name of the category
	cat_description = models.CharField(maxlength=255,blank=True, verbose_name="Short Description") # short description
	cat_depth = models.PositiveSmallIntegerField(default=0, choices=DEPTH, verbose_name="Category Tree Depth", help_text="Depth on tree like lists on WikiPages") # depth of the category in a tree, used by CSS :)
	class Meta:
		verbose_name = "Wiki Category"
		verbose_name_plural = "Wiki Categories"
	class Admin:
		list_display = ('cat_name', 'cat_description', 'cat_parent')
	def __str__(self):
		return self.cat_name

# Table with ContentBBCode descriptions that show on add/edit pages
class Cbc(models.Model):
	tag = models.CharField(maxlength=10, unique=True, verbose_name='Tag Name', help_text='The name of the ContentBBCode Tag ([rk:TAGNAME ****])') # tag name
	tag_example = models.CharField(maxlength=255, verbose_name="Example Tag", help_text='An example tag construct', unique=True) # example
	description = models.TextField(verbose_name='Tag Description', help_text='What this CBC does and how to use it') # full description
	class Admin:
		list_display = ('tag', 'description')
		search_fields = ['tag', 'description']
	class Meta:
		verbose_name = "Wiki CBC Description"
		verbose_name_plural = "Wiki CBC Descriptions"
	def __str__(self):
		return self.tag

#Wiki News
class News(models.Model):
	objects = CurrentSiteManager()
	site = models.ForeignKey(Site, blank = True, default=settings.SITE_ID)
	news_title = models.CharField(maxlength=255, verbose_name='News Title') 
	news_text = models.TextField(verbose_name='News Content')
	news_date = models.DateTimeField(auto_now_add = True)
	categories = models.ManyToManyField(WikiCategory, filter_interface=models.HORIZONTAL, verbose_name='News Categories')
	class Meta:
		verbose_name = "Wiki News"
		verbose_name_plural = "Wiki News"
	class Admin:
		list_display = ('news_title', 'news_date')
		list_filter = ['news_date']
		search_fields = ['news_title', 'news_text']
		date_hierarchy = 'news_date'
	def __str__(self):
		return self.news_title

#Wiki Bans
class Ban(models.Model):
	BAN = (
	('ip', 'IP'),
	('dns', 'DNS'),
	)
	ban_type = models.CharField(maxlength=255, verbose_name='Ban Type', help_text = 'Is it IP or hostname', default='ip', choices=BAN)
	ban_item = models.CharField(maxlength=255, verbose_name='Ban Item', help_text = 'The IP, IP range or hostname to ban', unique=True)
	ban_comment = models.CharField(maxlength=255, verbose_name='Comments', blank=True)
	class Meta:
		verbose_name = "Wiki Ban"
		verbose_name_plural = "Wiki Bans"
	class Admin:
		list_display = ('ban_item', 'ban_type', 'ban_comment')
		list_filter = ['ban_type']
		search_fields = ['ban_item', 'ban_comment']
	def __str__(self):
		return self.ban_item

# WikiPages
class Page(models.Model):
	objects = CurrentSiteManager()
	site = models.ForeignKey(Site, blank = True, default=settings.SITE_ID)
	title = models.CharField(maxlength=255) # page real title (for title tag and h1 in templates)
	slug = models.SlugField(maxlength=255, unique=True) # the wiki URL "title"
	description = models.CharField(maxlength=255) # short description (meta description, some link generation)
	text = models.TextField() # the page text
	changes = models.CharField(maxlength=255) # description of changes, no blanks!
	creation_date = models.DateTimeField(auto_now_add = True)
	modification_date = models.DateTimeField(auto_now = True)
	modification_user = models.CharField(maxlength=30)
	modification_ip = models.CharField(maxlength=20)
	modification_host = models.CharField(maxlength=100)
	categories = models.ManyToManyField(WikiCategory)
	class Meta:
		permissions = (("can_view", "Can view Page"), ("can_set_current", "Can set Page as current"))
		verbose_name = "WikiPage"
		verbose_name_plural = "WikiPages"
	def get_absolute_url(self):
		return '/wiki/page/' + self.slug + '/'
	def __str__(self):
		return str(self.id)

# table for old and to-aprove versions of WikiPages
class Archive(models.Model):
	objects = CurrentSiteManager()
	site = models.ForeignKey(Site, blank = True, default=settings.SITE_ID)
	page_id = models.ForeignKey(Page) # ID of the source page
	title = models.CharField(maxlength=255) # page real title (for title tag and h1 in templates)
	slug = models.SlugField(maxlength=255) # the wiki URL "title"
	description = models.CharField(maxlength=255) # short description (meta description, some link generation)
	text = models.TextField() # the page text
	changes = models.CharField(maxlength=255) # description of changes, no blanks!
	modification_date = models.DateTimeField()
	modification_user = models.CharField(maxlength=30)
	modification_ip = models.CharField(maxlength=20)
	modification_host = models.CharField(maxlength=100)
	is_proposal = models.BooleanField(blank=True, default=False) # is a changeset a proposal - when user can't set it as a current ver.
	class Meta:
		verbose_name = "WikiPage Archive"
		verbose_name_plural = "WikiPages Archive"
