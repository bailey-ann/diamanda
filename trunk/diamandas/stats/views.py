from django.shortcuts import render_to_response
from stats.models import *
from django.conf import settings
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

# unique entries
def entries(request):
	if request.user.is_authenticated() and request.user.has_perm('stats.add_stat'):
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
		return render_to_response('stats/entries.html', {'results': results})
	return render_to_response('stats/noperm.html', {'why': _('You don\'t have the permissions to view this page')})

# non google/se referers
def referers(request):
	if request.user.is_authenticated() and request.user.has_perm('stats.add_stat'):
		refs = Stat.objects.order_by('-id').exclude(referer__icontains='rk.edu.pl').exclude(referer__icontains='kibice.net').exclude(referer__icontains='insuran').exclude(referer__icontains='medic').exclude(referer__icontains='casino').exclude(referer__icontains='google').exclude(referer__icontains='msn.com').exclude(referer__icontains='onet.pl').exclude(referer__icontains='netsprint.pl').filter(referer__icontains='http://').values('referer')[:100]
		return render_to_response('stats/refs.html', {'refs': refs})
	return render_to_response('stats/noperm.html', {'why': _('You don\'t have the permissions to view this page')})

# google keywords
def google(request):
	if request.user.is_authenticated() and request.user.has_perm('stats.add_stat'):
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
		
		return render_to_response('stats/google.html', {'refs': results, 'google': google_pr})
	return render_to_response('stats/noperm.html', {'why': _('You don\'t have the permissions to view this page')})

# main page
def mainpage(request):
	return render_to_response('stats/mainpage.html', {'theme': settings.THEME, 'engine': settings.ENGINE})
#delete all data
def delete_all(request):
	Stat.objects.all().delete()
	return HttpResponseRedirect('/')