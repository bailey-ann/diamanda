#!/usr/bin/python
# Diamanda Application Set
# Polls
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils.translation import ugettext as _


class Poll(models.Model):
	question = models.CharField(max_length=200, verbose_name=_('Question'))
	class Meta:
		verbose_name = _('Poll')
		verbose_name_plural = _('Polls')
		db_table = 'rk_poll' + str(settings.SITE_ID)
	class Admin:
		list_display = ('question', )

class Choice(models.Model):
	poll = models.ForeignKey(Poll, edit_inline=models.TABULAR, num_in_admin=5)
	choice = models.CharField(max_length=200, verbose_name=_('Option'), core=True, blank=True)
	votes = models.IntegerField(verbose_name=_('Votes'), core=True, blank=True, default=0)
	class Meta:
		verbose_name = _('Option')
		verbose_name_plural = _('Options')
		db_table = 'rk_choice' + str(settings.SITE_ID)

class Vote(models.Model):
	poll = models.ForeignKey(Poll)
	voter = models.ForeignKey(User)
	class Meta:
		db_table = 'rk_vote' + str(settings.SITE_ID)

class PollComment(models.Model):
	content = models.ForeignKey(Poll)
	text = models.TextField(verbose_name=_('Text'))
	author = models.ForeignKey(User)
	date = models.DateTimeField(default=datetime.now)
	class Meta:
		db_table = 'rk_pollcomment' + str(settings.SITE_ID)