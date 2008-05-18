#!/usr/bin/python
# Diamanda Application Set
# User Panel
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.ForeignKey(User, unique=True)
	onsitedata = models.DateTimeField(default=datetime.now(), blank=True)
	def __str__(self):
		return str(self.user)
	def __unicode__(self):
		return unicode(self.user)
	def save(self, **kwargs):
		"""override save to set defaults"""
		if self.pk:
			self.onsitedata = datetime.now()
		super(Profile, self).save(**kwargs)