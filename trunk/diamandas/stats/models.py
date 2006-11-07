from django.db import models

class Stat(models.Model):
	ip = models.IPAddressField()
	referer = models.TextField()
	date = models.CharField(maxlength=10, blank=True)
	class Meta:
		verbose_name = _('Stat')
		verbose_name_plural = _('Stats')
	def __str__(self):
		return self.ip
