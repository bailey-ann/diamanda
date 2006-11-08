from django.shortcuts import render_to_response
from stats.models import *
from django.conf import settings
from datetime import datetime
from pylab import *
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

# unique entries
def entries(request):
	if request.user.is_authenticated() and request.user.has_perm('stats.add_stat'):
		today = str(datetime.today())[:10]
		#tday = int(today[8:10])
		tday = 31
		x = []
		y = []
		while tday > 0:
			if tday < 10:
				txday = today[0:7] + '-0' + str(tday)
			else:
				txday = today[0:7] + '-' + str(tday)
			x.append(int(tday))
			y.append(int(Stat.objects.filter(date = txday).count()))
			tday = tday -1
		xlabel(_('Day of month'))
		ylabel(_('Number of entries'))
		title('Unique Entries in this month')
		
		a, b = polyfit(x, y, 1)
		y2 = []
		for i in x:
			y2.append(a*i+b)
		plot(x, y, 'r', x, y2, 'b')
		savefig(settings.SITE_IMAGES_DIR_PATH  + 'uniqueentries.png')
		return render_to_response('stats/' + settings.ENGINE + '/entries.html', {'theme': settings.THEME, 'engine': settings.ENGINE, 'img_path': settings.SITE_IMAGES_SRC_PATH})
	return render_to_response('stats/' + settings.ENGINE + '/noperm.html', {'why': _('You don\'t have the permissions to view this page'), 'theme': settings.THEME, 'engine': settings.ENGINE})

# non google/se referers
def referers(request):
	if request.user.is_authenticated() and request.user.has_perm('stats.add_stat'):
		sitename = Site.objects.get(id=settings.SITE_ID)
		refs = Stat.objects.order_by('-id').exclude(referer__icontains=sitename).exclude(referer__icontains='google').exclude(referer__icontains='msn.com').exclude(referer__icontains='onet.pl').exclude(referer__icontains='netsprint.pl').values('referer')[:100]
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
		return render_to_response('stats/' + settings.ENGINE + '/google.html', {'theme': settings.THEME, 'engine': settings.ENGINE, 'refs': results})
	return render_to_response('stats/' + settings.ENGINE + '/noperm.html', {'why': _('You don\'t have the permissions to view this page'), 'theme': settings.THEME, 'engine': settings.ENGINE})

#delete all data
def delete_all(request):
	Stat.objects.all().delete()
	return HttpResponseRedirect('/')