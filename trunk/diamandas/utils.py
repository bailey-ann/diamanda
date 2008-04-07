#!/usr/bin/python
# Diamanda Application Set
# Utils

from django.shortcuts import render_to_response
from django.template import RequestContext

def redirect_by_template(request, redirect_to, msg):
	return render_to_response('pages/msg.html', {'msg': msg, 'redirect_to': redirect_to}, context_instance=RequestContext(request))


