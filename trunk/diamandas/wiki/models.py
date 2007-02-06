from django.db import models
from django.contrib.auth.models import User

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
		return '/w/p/' + self.slug + '/'
	def __str__(self):
		return self.slug
	def save(self):
		# save old version of page to the archive if exists.
		try:
			page = Page.objects.get(slug=self.slug)
		except:
			pass
		else:
			old = Archive(page_id = self, title=page.title, description = page.description, text=page.text, changes = page.changes, modification_date = page.modification_date, modification_user = page.modification_user, modification_ip = page.modification_ip)
			old.save()
		super(Page, self).save()
		

# table for old and to-aprove versions of WikiPages
class Archive(models.Model):
	page_id = models.ForeignKey(Page) # ID of the source page
	title = models.CharField(maxlength=255) # page real title (for title tag and h1 in templates)
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
