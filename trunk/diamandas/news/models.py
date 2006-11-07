from django.db import models
from os import listdir
from django.conf import settings

class Keywords(models.Model):
	name = models.CharField(maxlength=255, verbose_name=_('Keyword Name'))
	class Meta:
		verbose_name = _('Keyword')
		verbose_name_plural = _('Keywords')
	class Admin:
		list_display = ('name',)
	def __str__(self):
		return self.name

class News(models.Model):
	i = listdir(settings.SITE_IMAGES_DIR_PATH + 'icons/')
	
	ICONS = [['-', '-']]
	for ic in i:
		ICONS.append([ic, ic])
	
	news_title = models.CharField(maxlength=255, verbose_name=_('Title'))
	news_text = models.TextField(verbose_name=_('Text'))
	news_more = models.TextField(verbose_name=_('Extended Text'), blank=True, default='')
	news_date = models.DateTimeField(auto_now_add = True)
	news_keywords = models.ManyToManyField(Keywords, verbose_name=_('Keywords'))
	news_icon = models.CharField(maxlength=255, verbose_name=_('Icon'), choices=ICONS, default='-')
	class Meta:
		verbose_name = _('News')
		verbose_name_plural = _('News')
	class Admin:
		list_display = ('news_title', 'news_date')
		list_filter = ['news_date']
		search_fields = ['news_title', 'news_text']
		date_hierarchy = 'news_date'
		fields = (
		(None, {
		'fields': ('news_title', 'news_text', 'news_keywords', 'news_icon')
		}),
		(_('Extended Text'), {
		'classes': 'collapse',
		'fields' : ('news_more',)
		}),)
	def __str__(self):
		return self.news_title

