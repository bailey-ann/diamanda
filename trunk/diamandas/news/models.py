from django.db import models
from django.conf import settings

class News(models.Model):
	news_title = models.CharField(maxlength=255, verbose_name=_('Title'))
	news_slug = models.SlugField(maxlength=255, unique=True, prepopulate_from=("news_title", ), verbose_name='Slug') # the wiki URL "title"
	news_text = models.TextField(verbose_name=_('Text'))
	news_date = models.DateTimeField(auto_now = True)
	class Meta:
		verbose_name = _('News')
		verbose_name_plural = _('News')
		db_table = 'rk_news' + str(settings.SITE_ID)
	class Admin:
		list_display = ('news_title', 'news_date')
		list_filter = ['news_date']
		search_fields = ['news_title', 'news_text']
		date_hierarchy = 'news_date'
	def get_absolute_url(self):
		return '/news/more/' + str(self.id) + '/'
	def __str__(self):
		return self.news_title

