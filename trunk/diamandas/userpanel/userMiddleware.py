#!/usr/bin/python
# Diamanda Application Set
# User Panel

from datetime import timedelta
from datetime import datetime

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login

from userpanel.models import *

class userMiddleware(object):
	"""
	Update user onsitedata when he is on site (to display "users online")
	Handle OpenID association
	"""
	def process_request(self, request):
		if request.openid and str(request.openid).find('.') != -1 and not request.user.is_authenticated():
			request.session['new_openid'] = False
			try:
				o = OpenIdAssociation.objects.get(openid=str(request.openid))
			except:
				request.session['new_openid'] = True
			else:
				# block openID - user authentication for staff
				if not o.user.is_staff:
					user = authenticate(user_id = o.user.id, openid=str(request.openid))
					if user is not None:
						login(request, user)
		
		if request.user.is_authenticated():
			now = datetime.now()
			check_time = now - timedelta(minutes=10)
			if not request.session.__contains__('onsite') or request.session['onsite'] < check_time:
				request.session['onsite'] = now
				try:
					a = Profile.objects.get(user=request.user)
					a.save()
				except:
					a = Profile(user=request.user)
					a.save()
