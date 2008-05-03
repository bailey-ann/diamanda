from django.conf import settings
from pages.models import *


def bib(request):
	books = Content.objects.filter(content_type='book', book_order__gt=0).order_by('book_order').values('slug', 'title')
	return {'sid': settings.SITE_ID, 'domain': settings.SITE_KEY, 'books': books, 'site_name': settings.SITE_NAME, 'site_desc': settings.SITE_DESCRIPTION}