from django.db import models
from django.conf import settings

class Task(models.Model):
	STATUSS = (
	(_('Open'), _('Open')),
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
	task_text = models.TextField(verbose_name=_('Task Description'))
	task_status = models.CharField(maxlength=255, choices=STATUSS, verbose_name=_('Task Status'))
	task_creation_date = models.DateTimeField(auto_now_add = True, verbose_name=_('Creation Date'), blank=True)
	task_modification_date = models.DateTimeField(auto_now = True, verbose_name=_('Modification Date'), blank=True)
	task_progress = models.CharField(maxlength=255, choices=PROGRESS, verbose_name=_('Progress'), default='0')
	is_sticky = models.BooleanField(blank=True, default=False, verbose_name=_('Sticky'))
	class Meta:
		verbose_name = _('Task')
		verbose_name_plural = _('Site Tasks')
	class Admin:
		list_display = ('task_name', 'task_status', 'task_progress')
		search_fields = ['task_name', 'task_text']
	def __str__(self):
		return self.task_name
# Task comments
class TaskComment(models.Model):
	com_task_id = models.ForeignKey(Task) # ID of the task
	com_text = models.TextField(verbose_name=_('Comment'))
	com_author = models.CharField(maxlength=255, verbose_name=_('Author'), blank=True)
	com_date = models.DateTimeField(auto_now_add = True)
	com_ip = models.CharField(maxlength=20, blank=True)
	class Meta:
		verbose_name = _('Task Comment')
		verbose_name_plural = _('Task Comments')
	def __str__(self):
		return str(self.id)