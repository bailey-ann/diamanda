#!/usr/bin/python
# Diamanda Application Set
# Gettext files translation statistics

from os import remove
import polib

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Translation(models.Model):
	pofile = models.FileField(verbose_name=_('PO file for translation'), upload_to='resources/' + settings.SITE_KEY + '/translations')
	name = models.CharField(max_length=255, verbose_name=_('Application name'))
	description = models.CharField(max_length=255, verbose_name=_('Description'))
	lang = models.CharField(max_length=100, verbose_name=_('Language of Translation'), choices=(('pl', 'Polski'), ('en', 'English')))
	percent_translated =  models.PositiveIntegerField(default=0, blank=True, null=True)
	fuzzy_entries =  models.PositiveIntegerField(default=0, blank=True, null=True)
	untrans_entries =  models.PositiveIntegerField(default=0, blank=True, null=True)
	trans_entries =  models.PositiveIntegerField(default=0, blank=True, null=True)
	translator = models.ForeignKey(User, blank=True, null=True, verbose_name=_('Translator'))
	class Meta:
		verbose_name = _('Translation')
		verbose_name_plural = _('Translations')
		db_table = 'rk_tra' + str(settings.SITE_ID)
	class Admin:
		list_display = ('name', 'pofile', 'translator')
		search_fields = ['name', 'description']
		fields = (
		(_('Gettext Translation File Informations'), {
		'fields': ('pofile', 'name', 'description', 'lang', 'translator')
		}),)
	def get_absolute_url(self):
		return '/tra/show/' + str(self.id) + '/'
	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name
	def save(self):
		try:
			tra = Translation.objects.get(id=self.id)
		except:
			pass
		else:
			if self.pofile != tra.pofile:
				remove(settings.MEDIA_ROOT + tra.pofile)
		super(Translation, self).save()
		tra = Translation.objects.get(id=self.id)
		po = polib.pofile(settings.MEDIA_ROOT + tra.pofile)
		percent_translated = po.percent_translated()
		fuzzy_entries = len(po.fuzzy_entries())
		untrans_entries = len(po.untranslated_entries())
		trans_entries= len(po.translated_entries())
		if percent_translated != tra.percent_translated or fuzzy_entries != tra.fuzzy_entries or untrans_entries != tra.untrans_entries or trans_entries != tra.trans_entries:
			tra.percent_translated = po.percent_translated()
			tra.fuzzy_entries = len(po.fuzzy_entries())
			tra.untrans_entries = len(po.untranslated_entries())
			tra.trans_entries = len(po.translated_entries())
			tra.save()