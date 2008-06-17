#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
from postmarkup import render_bbcode

from django.http import HttpResponse

def bbcode(request):
	"""
	BBCode Preview for MarkitUp editor
	"""
	if 'data' in request.POST:
		data = render_bbcode(request.POST['data'], "UTF-8")
	else:
		data = ''
	return HttpResponse(data)
