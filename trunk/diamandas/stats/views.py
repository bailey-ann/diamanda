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
		return render_to_response('stats/' + settings.ENGINE + '/entries.html', {'theme': settings.THEME, 'engine': settings.ENGINE, 'results': results})
	return render_to_response('stats/' + settings.ENGINE + '/noperm.html', {'why': _('You don\'t have the permissions to view this page'), 'theme': settings.THEME, 'engine': settings.ENGINE})

# non google/se referers
def referers(request):
	if request.user.is_authenticated() and request.user.has_perm('stats.add_stat'):
		refs = Stat.objects.order_by('-id').exclude(referer__icontains='rk.edu.pl').exclude(referer__icontains='kibice.net').exclude(referer__icontains='insuran').exclude(referer__icontains='medic').exclude(referer__icontains='casino').exclude(referer__icontains='google').exclude(referer__icontains='msn.com').exclude(referer__icontains='onet.pl').exclude(referer__icontains='netsprint.pl').filter(referer__icontains='http://').values('referer')[:100]
		return render_to_response('stats/' + settings.ENGINE + '/refs.html', {'theme': settings.THEME, 'engine': settings.ENGINE, 'refs': refs})
	return render_to_response('stats/' + settings.ENGINE + '/noperm.html', {'why': _('You don\'t have the permissions to view this page'), 'theme': settings.THEME, 'engine': settings.ENGINE})

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
		
		jaki = refs = float(Stat.objects.filter(referer__icontains='jakilinux').count())
		jaki_pr = str((jaki/all_links)*100)[0:5]
		
		wykop = refs = float(Stat.objects.filter(referer__icontains='wykop').count())
		wykop_pr = str((wykop/all_links)*100)[0:5]
		
		wiki = refs = float(Stat.objects.filter(referer__icontains='wikipedia').count())
		wiki_pr = str((wiki/all_links)*100)[0:5]
		
		return render_to_response('stats/' + settings.ENGINE + '/google.html', {'theme': settings.THEME, 'engine': settings.ENGINE, 'refs': results, 'google': google_pr, 'jaki': jaki_pr, 'wykop': wykop_pr, 'wiki': wiki_pr})
	return render_to_response('stats/' + settings.ENGINE + '/noperm.html', {'why': _('You don\'t have the permissions to view this page'), 'theme': settings.THEME, 'engine': settings.ENGINE})

# main page
def mainpage(request):
	return render_to_response('stats/' + settings.ENGINE + '/mainpage.html', {'theme': settings.THEME, 'engine': settings.ENGINE})
#delete all data
def delete_all(request):
	Stat.objects.all().delete()
	return HttpResponseRedirect('/')