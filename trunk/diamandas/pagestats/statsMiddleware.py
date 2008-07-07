#!/usr/bin/python
# Diamanda Application Set
# Simple stats

from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect

from diamandas.pagestats.models import *

class statsMiddleware(object):
	"""
	Log stats data
	"""
	def process_request(self, request):
		if 'HTTP_USER_AGENT' in request.META:
			a = request.META['HTTP_USER_AGENT'].lower()
		else:
			a = '--'
		if a.find('httrack') != -1 or a.find('teleport') != -1 or a.find('wget') != -1 or a.find('copier') != -1:
			return HttpResponse('Bez klonowania strony!')
		if not 'stats' in request.session:
			try:
				today = str(datetime.today())[:10]
				unique = Stat.objects.filter(ip = request.META['REMOTE_ADDR'], date = today).count()
				if unique < 1:
					if not request.META.has_key('HTTP_REFERER'):
						request.META['HTTP_REFERER'] = ''
					else:
						request.META['HTTP_REFERER'] = request.META['HTTP_REFERER'].decode('utf-8')
					s = Stat(ip = request.META['REMOTE_ADDR'], referer = request.META['HTTP_REFERER'], date = today)
					s.save()
			except:
				pass
			request.session['stats'] = 'ok'