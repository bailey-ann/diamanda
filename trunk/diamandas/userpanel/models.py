from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	username = models.ForeignKey(User)
	email = models.EmailField() # user email to be shown/used
	signature = models.CharField(maxlength=255, verbose_name="Signature", blank=True, default='') # user sig
	contacts = models.CharField(maxlength=255, verbose_name="Contacts", blank=True, default='') # contacts
	public_info = models.TextField(verbose_name="Public Info", blank=True, default='') # contacts
	def __str__(self):
		return str(self.username)
