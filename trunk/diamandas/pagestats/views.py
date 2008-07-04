#!/usr/bin/python
# Diamanda Application Set
# Simple stats

from datetime import datetime

from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from pagestats.models import *


def entries(request):
	"""
	return unique entries in days
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		today = str(datetime.today())[:10]
		tday = int(today[8:10])
		results = []
		while tday > 0:
			if tday < 10:
				txday = today[0:7] + '-0' + str(tday)
			else:
				txday = today[0:7] + '-' + str(tday)
			results.append({'day':txday, 'count':Stat.objects.filter(date = txday).count()})
			tday = tday -1
		return render_to_response('stats/entries.html', {'results': results}, context_instance=RequestContext(request))
	return render_to_response(
		'pages/bug.html',
		{'bug': _('You don\'t have the permissions to view this page')},
		context_instance=RequestContext(request))


def referers(request):
	"""
	return non SE/google referers
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		refs = Stat.objects.order_by('-id')
		refs = refs.exclude(referer__icontains=settings.SITE_KEY)
		refs = refs.exclude(referer__icontains='google')
		refs = refs.exclude(referer__icontains='yahoo')
		refs = refs.exclude(referer__icontains='msn.com')
		refs = refs.exclude(referer__icontains='onet.pl')
		refs = refs.exclude(referer__icontains='netsprint.pl')
		refs = refs.filter(referer__icontains='http://').values('referer')[:100]
		return render_to_response('stats/refs.html', {'refs': refs}, context_instance=RequestContext(request))
	return render_to_response('pages/bug.html', {'bug': _('You don\'t have the permissions to view this page')}, context_instance=RequestContext(request))


def google(request):
	"""
	return list of google keywords
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		refs = Stat.objects.order_by('-id').filter(referer__icontains='google').values('referer')
		words = []
		words_keys = {}
		for i in refs:
			r = i['referer'].lower().split('q=')
			if len(r) > 1:
				r = r[1]
				word = r.split('&')[0]
				words.append(word)
				words_keys[word] = True
		if len(words) < 1:
			return render_to_response(
				'stats/google.html',
				{'error': True},
				context_instance=RequestContext(request))
		words_keys = words_keys.keys()
		results = []
		for w in words_keys:
			cnt = words.count(w)
			if cnt > 5 and len(w) > 2:
				results.append({'word': w, 'count':cnt})
		results.sort()
		
		google_links = float(len(refs))
		all_links = refs = float(Stat.objects.all().count())
		google_pr = str((google_links/all_links)*100)[0:5]
		
		wiki = refs = float(Stat.objects.filter(referer__icontains='wikipedia').count())
		wiki_pr = str((wiki/all_links)*100)[0:5]
		
		return render_to_response(
			'stats/google.html',
			{'refs': results, 'google': google_pr, 'wiki': wiki_pr},
			context_instance=RequestContext(request))
	return render_to_response('pages/bug.html', {'bug': _('You don\'t have the permissions to view this page')}, context_instance=RequestContext(request))


def mainpage(request):
	"""
	main page
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		return render_to_response('stats/mainpage.html', context_instance=RequestContext(request))
	else:
		return render_to_response('pages/bug.html', {'bug': _('You don\'t have the permissions to view this page')}, context_instance=RequestContext(request))


def delete_all(request):
	"""
	delete all data
	"""
	if request.user.is_authenticated() and request.user.is_staff:
		Stat.objects.all().delete()
	return HttpResponseRedirect('/')