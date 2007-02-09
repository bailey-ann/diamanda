from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	username = models.ForeignKey(User)
	email = models.EmailField() # user email to be shown
	public_info = models.TextField(verbose_name="Public Info", blank=True, default='') # contacts
	def __str__(self):
		return str(self.username)
