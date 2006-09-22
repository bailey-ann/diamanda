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

#Wiki Bans
class Ban(models.Model):
	BAN = (
	('ip', 'IP'),
	('dns', 'DNS'),
	)
	ban_type = models.CharField(maxlength=255, verbose_name=_('Ban Type'), help_text = _('Is it IP or hostname'), default='ip', choices=BAN)
	ban_item = models.CharField(maxlength=255, verbose_name=_('Ban Item'), help_text = _('The IP, IP range or hostname to ban'), unique=True)
	ban_comment = models.CharField(maxlength=255, verbose_name=_('Comments'), blank=True)
	class Meta:
		verbose_name = _('Wiki Ban')
		verbose_name_plural = _('Wiki Bans')
	class Admin:
		list_display = ('ban_item', 'ban_type', 'ban_comment')
		list_filter = ['ban_type']
		search_fields = ['ban_item', 'ban_comment']
	def __str__(self):
		return self.ban_item

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
	modification_host = models.CharField(maxlength=100, blank=True)
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
	modification_host = models.CharField(maxlength=100, blank=True)
	is_proposal = models.BooleanField(blank=True, default=False) # is a changeset a proposal - when user can't set it as a current ver.
	class Meta:
		verbose_name = _('WikiPage Archive')
		verbose_name_plural = _('WikiPages Archive')

# Tasks
class Task(models.Model):
	TYPES = (
	(_('Site Content'), _('Site Content')),
	(_('Technical Issues'), _('Technical Issues')),
	(_('Site in the Web'), _('Site in the Web')),
	(_('Other'), _('Other')),
	)
	STATUSS = (
	(_('Unassigned'), _('Unassigned')),
	(_('Assigned'), _('Assigned')),
	(_('Closed'), _('Closed')),
	)
	PROGRESS = (
	('0', _('Nothing Done Yet')),
	('25', _('25% Done')),
	('50', _('50% Done')),
	('75', _('75% Done')),
	('100', _('Task Completed')),
	)
	task_name = models.CharField(maxlength=255, verbose_name=_('Task Title'))
	task_type = models.CharField(maxlength=255, choices=TYPES, verbose_name=_('Task Type'))
	task_text = models.TextField(verbose_name=_('Task Description'))
	task_status = models.CharField(maxlength=255, choices=STATUSS, verbose_name=_('Task Status'))
	task_assignedto = models.ManyToManyField(User, verbose_name=_('Assigned To'), blank=True, default='')
	task_creation_date = models.DateTimeField(auto_now_add = True, verbose_name=_('Creation Date'))
	task_modification_date = models.DateTimeField(auto_now = True, verbose_name=_('Modification Date'))
	task_progress = models.CharField(maxlength=255, choices=PROGRESS, verbose_name=_('Progress'))
	class Meta:
		verbose_name = _('Task')
		verbose_name_plural = _('Wiki Tasks')
	class Admin:
		list_display = ('task_name', 'task_status', 'task_progress')
		search_fields = ['task_name', 'task_text']
	def __str__(self):
		return self.task_name
