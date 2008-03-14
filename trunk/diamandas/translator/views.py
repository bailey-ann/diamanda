#!/usr/bin/python
# Diamanda Application Set
# Gettext files translation statistics

import polib

from django.shortcuts import render_to_response
from django import oldforms as forms
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _

from translator.models import *
from boxcomments.models import Comment
from translator.context import translator as translatorContext

def tra_list(request):
	"""
	List all translations
	"""
	tra = Translation.objects.all().order_by('percent_translated')
	return render_to_response('translator/tra_list.html', {'tra':  tra}, context_instance=RequestContext(request, translatorContext(request)))

def tra_show(request, tid):
	"""
	Show translation info
	
	* tid - ID of an Translation entry
	"""
	try:
		tra = Translation.objects.get(id=tid)
	except:
		return render_to_response('pages/bug.html', {'bug': _('Translation doesn\'t exist')}, context_instance=RequestContext(request, translatorContext(request)))
	
	if tra.percent_translated != 100 and tra.untrans_entries < 100:
		po = polib.pofile(settings.MEDIA_ROOT + tra.pofile)
		untrans = po.untranslated_entries()
		fuzzy = po.fuzzy_entries()
		return render_to_response(
			'translator/tra_show.html',
			{'tra':  tra, 'untrans': untrans, 'fuzzy': fuzzy, 'com': Comment.objects.filter(apptype= 4, appid = tid).count()},
			context_instance=RequestContext(request, translatorContext(request)))
	return render_to_response(
		'translator/tra_show.html',
		{'tra':  tra, 'com': Comment.objects.filter(apptype= 4, appid = tid).count()},
		context_instance=RequestContext(request, translatorContext(request)))

def tra_apply(request, tid):
	"""
	Set user as a maintainer of a translation
	
	* tid - ID of an Translation entry
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/user/login/')
	else:
		tra = Translation.objects.get(id=tid)
		if not tra.translator:
			tra.translator = request.user
			tra.save()
		return HttpResponseRedirect('/tra/show/' + str(tid) + '/')

def get_po(request, tid):
	"""
	Download translation
	
	* tid - ID of an Translation entry
	"""
	try:
		tra = Translation.objects.values('pofile').get(id=tid)
	except:
		return render_to_response('pages/bug.html', {'bug': _('Translation doesn\'t exist')}, context_instance=RequestContext(request, translatorContext(request)))
	po = open(settings.MEDIA_ROOT + tra['pofile']).read()
	e = HttpResponse()
	e['Content-Type'] = 'application/x-gettext'
	e['Content-Disposition'] = 'attachment; filename="' + tra['pofile'] + '";'
	e.write(po)
	return e
	

def translations(request):
	"""
	Show Gettext help
	"""
	return render_to_response('translator/tra.html', context_instance=RequestContext(request, translatorContext(request)))