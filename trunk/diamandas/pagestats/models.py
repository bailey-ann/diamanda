#!/usr/bin/python
# Diamanda Application Set
# Simple stats

from django.db import models
from django.utils.translation import ugettext as _

class Stat(models.Model):
	ip = models.IPAddressField()
	referer = models.TextField(blank=True, null=True)
	date = models.CharField(max_length=10)
	class Meta:
		verbose_name = _('Stat')
		verbose_name_plural = _('Stats')
	def __str__(self):
		return self.referer
	def __unicode__(self):
		return self.referer
