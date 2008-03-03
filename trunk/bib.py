from django.conf import settings

def bib(request):
	return {'sid': settings.SITE_ID, 'domain': settings.SITE_KEY}