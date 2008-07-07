#!/usr/bin/python
# Diamanda Application Set
# TEMPLATE_CONTEXT_PROCESSOR

from django.conf import settings
from diamandas.pages.models import Content


def bib(request):
	books = Content.objects.filter(content_type='book', book_order__gt=0).order_by('book_order').values('slug', 'title')
	if 'new_openid' in request.session and request.session['new_openid'] == True:
		new_openid = True
		openid = request.openid
	else:
		new_openid = False
		openid = False
	return {'sid': settings.SITE_ID, 'domain': settings.SITE_DOMAIN, 'books': books, 'siteName': settings.SITE_NAME, 'site_desc': settings.SITE_DESCRIPTION,
			'new_openid': new_openid, 'openid': request.openid}