#!/usr/bin/python
# Diamanda Application Set
# Simple stats

from stats.models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
#from django.db import connection
#from django.template import Template, Context

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
	#def process_response( self, request, response ):
		#time = 0.0
		#for q in connection.queries:
			#time += float(q['time'])
		#t = Template('''
		#<p><em>Total query count:</em> {{ count }}<br/>
		#<em>Total execution time:</em> {{ time }}</p>
		#<ul class="sqllog">
			#{% for sql in sqllog %}
			#<li>{{ sql.time }}: {{ sql.sql }}</li>
			#{% endfor %}
		#</ul>
		#''')
		#response.content = "%s%s" % ( response.content, t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time})))
		#return response


