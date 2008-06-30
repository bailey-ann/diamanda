#!/usr/bin/python
# Diamanda Application Set
# User Panel

from django.contrib.auth.models import User
from django.conf import settings

from userpanel.models import *

class OpenIdBackend:
	"""
	Authenticate a user that has associated OpenID to his account
	"""
	def authenticate(self, user_id=False, openid=False):
		if user_id and openid:
			try:
				o = OpenIdAssociation.objects.get(openid=openid, user=User.objects.get(id=user_id))
				return o.user
			except:
				return None
		return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None