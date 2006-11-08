from stats.models import *
from datetime import datetime

class statsMiddleware(object):
	def process_request(self, request):
		try:
			today = str(datetime.today())[:10]
			unique = Stat.objects.filter(ip = request.META['REMOTE_ADDR'], date = today).count()
			if unique < 1:
				if not request.META.has_key('HTTP_REFERER'):
					request.META['HTTP_REFERER'] = ''
				s = Stat(ip = request.META['REMOTE_ADDR'], referer = request.META['HTTP_REFERER'], date = today)
				s.save()
		except:
			pass


