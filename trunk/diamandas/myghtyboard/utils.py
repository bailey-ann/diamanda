#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
from diamandas.myghtyboard.templatetags.fbc import fbc

from django.http import HttpResponse

def bbcode(request):
	"""
	BBCode Preview for MarkitUp editor
	"""
	if 'data' in request.POST:
		data = fbc(request.POST['data'])
	else:
		data = ''
	return HttpResponse(data)
