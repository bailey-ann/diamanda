#!/usr/bin/python
# Diamanda Application Set
# User Panel
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Profile(models.Model):
	"""
	User Profile
	"""
	user = models.ForeignKey(User, unique=True)
	onsitedata = models.DateTimeField(default=datetime.now(), blank=True)
	last_visit = models.DateTimeField(default=datetime.now(), blank=True)
	def __str__(self):
		return str(self.user)
	def __unicode__(self):
		return unicode(self.user)
	def save(self, **kwargs):
		if self.pk:
			if not self.last_visit:
				self.last_visit = datetime.now()
			self.last_visit = self.onsitedata
			self.onsitedata = datetime.now()
		super(Profile, self).save(**kwargs)

class CaptchaToken(models.Model):
	"""
	Tokens for captcha questions
	- hides answer hash and prevents from reusing the same captcha by a bot
	"""
	answer = models.CharField(max_length=255)
	token = models.CharField(max_length=15)
	date = models.DateTimeField(default=datetime.now())
	def __str__(self):
		return self.token
	def __unicode__(self):
		return self.token

class OpenIdAssociation(models.Model):
	"""
	Assoction of user accounts and openIDs
	"""
	user = models.ForeignKey(User, verbose_name=_('User'), limit_choices_to={'is_staff': False})
	openid = models.CharField(max_length=255, verbose_name=_('OpenID'))
	def __str__(self):
		return self.openid
	def __unicode__(self):
		return self.openid
	class Meta:
		verbose_name = _('OpenID association')
		verbose_name_plural = _('OpenID associations')
	class Admin:
		list_display = ('openid', 'user')
		list_filter = ['openid', 'user']