#!/usr/bin/python
# Diamanda Application Set
# Boxcomments - global comment system

from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Comment(models.Model):
	title = models.CharField(max_length=255, blank=True)
	text = models.TextField(verbose_name=_('Text'))
	date = models.DateTimeField(default=datetime.now)
	apptype = models.PositiveSmallIntegerField()
	appid = models.PositiveIntegerField()
	author = models.CharField(max_length=255)
	ip = models.CharField(max_length=20, blank=True)
	class Meta:
		verbose_name = _('Comment')
		verbose_name_plural = _('Comments')
		db_table = 'rk_com' + str(settings.SITE_ID)
	class Admin:
		list_display = ('title', 'author')
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title