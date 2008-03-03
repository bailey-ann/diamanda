#!/usr/bin/python
# Diamanda Application Set
#GCodeSearch - Google code search GData Client

from httplib import HTTPConnection
import urllib
from xml.dom import minidom

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django import newforms as forms
from django.utils.translation import ugettext as _


class SearchForm(forms.Form):
	phrase = forms.CharField(label=_('Phrase'))

def search(request):
	"""
	Search google code database using GData
	"""
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			phrase = form.cleaned_data['phrase']
			con = HTTPConnection("google.com")
			con.putrequest('GET', '/codesearch/feeds/search?q=%s' % urllib.quote(phrase))
			con.endheaders()
			con.send('')
			r = con.getresponse()
			if str(r.status) == '200':
				DOMTree = minidom.parseString(r.read())
				nodes = DOMTree.childNodes
				data = nodes[0].getElementsByTagName('entry')
				result = []
				for i in data:
					code = []
					for c in i.getElementsByTagName('gcs:match'):
						code.append((c.getAttribute("lineNumber"), c.childNodes[0].toxml().replace('&lt;', '<').replace('&gt;', '>').replace('&#39', "'").replace('&quot;', '"').replace('&amp;', '&')))
					
					result.append({
						'link': i.getElementsByTagName('link')[0].getAttribute("href"),
						'filename': i.getElementsByTagName('title')[0].childNodes[0].toxml(),
						'code': code
						})
			else:
				print r.status
				result = False
			#soup = BeautifulStoneSoup(dane)
			#dane = soup.prettify()
			
			#result = False
			return render_to_response(
				'gcodesearch/search.html',
				{'form': form, 'result': result},
				context_instance=RequestContext(request))
		else:
			return render_to_response(
				'gcodesearch/search.html',
				{'form': form},
				context_instance=RequestContext(request))

	form =  SearchForm()

	return render_to_response(
		'gcodesearch/search.html',
		{'form': form},
		context_instance=RequestContext(request))