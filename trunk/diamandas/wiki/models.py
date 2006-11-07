from django.db import models
from django.contrib.auth.models import User

# Table with ContentBBCode descriptions that show on add/edit pages
class Cbc(models.Model):
	tag = models.CharField(maxlength=10, unique=True, verbose_name=_('Tag Name'), help_text=_('The name of the ContentBBCode Tag ([rk:TAGNAME ****])')) # tag name
	tag_example = models.CharField(maxlength=255, verbose_name=_('Example Tag'), help_text=_('An example tag construct'), unique=True) # example
	description = models.TextField(verbose_name=_('Tag Description'), help_text=_('What this CBC does and how to use it')) # full description
	class Admin:
		list_display = ('tag', 'description')
		search_fields = ['tag', 'description']
	class Meta:
		verbose_name = _('Wiki CBC Description')
		verbose_name_plural = _('Wiki CBC Descriptions')
	def __str__(self):
		return self.tag

# WikiPages
class Page(models.Model):
	title = models.CharField(maxlength=255) # page real title (for title tag and h1 in templates)
	slug = models.SlugField(maxlength=255, unique=True) # the wiki URL "title"
	description = models.CharField(maxlength=255) # short description (meta description, some link generation)
	text = models.TextField() # the page text
	changes = models.CharField(maxlength=255) # description of changes, no blanks!
	creation_date = models.DateTimeField(auto_now_add = True)
	modification_date = models.DateTimeField(auto_now = True)
	modification_user = models.CharField(maxlength=30)
	modification_ip = models.CharField(maxlength=20, blank=True)
	class Meta:
		permissions = (("can_view", "Can view Page"), ("can_set_current", "Can set Page as current"))
		verbose_name = _('WikiPage')
		verbose_name_plural = _('WikiPages')
	def get_absolute_url(self):
		return '/wiki/page/' + self.slug + '/'
	def __str__(self):
		return str(self.id)

# table for old and to-aprove versions of WikiPages
class Archive(models.Model):
	page_id = models.ForeignKey(Page) # ID of the source page
	title = models.CharField(maxlength=255) # page real title (for title tag and h1 in templates)
	slug = models.SlugField(maxlength=255) # the wiki URL "title"
	description = models.CharField(maxlength=255) # short description (meta description, some link generation)
	text = models.TextField() # the page text
	changes = models.CharField(maxlength=255) # description of changes, no blanks!
	modification_date = models.DateTimeField()
	modification_user = models.CharField(maxlength=30)
	modification_ip = models.CharField(maxlength=20, blank=True)
	is_proposal = models.BooleanField(blank=True, default=False) # is a changeset a proposal - when user can't set it as a current ver.
	class Meta:
		verbose_name = _('WikiPage Archive')
		verbose_name_plural = _('WikiPages Archive')
