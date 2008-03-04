# -*- coding: utf-8 -*-
#!/usr/bin/python
# Diamanda Application Set
# CBCParhaser - replace tags with some content

from os.path import isfile
from datetime import timedelta
from datetime import datetime
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from django.conf import settings

from pages.models import Content

def thumb(dic, text):
	"""
	display an image with a thumbnail and lightbox like script
	"""
	THUMB = '''<div style="text-align:center;">
<a href="/site_media/resources/%s.rk.edu.pl/images/%s" rel="thumbnail"><img src="/site_media/resources/%s.rk.edu.pl/images/%s" alt="%s" /></a>
</div>'''
	for i in dic:
		img = i['attributes']['src'].split('/')
		thumb = 'thumb_' + img[-1]
		im = img[-1]
		domain = img[0]
		if isfile(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + im):
			if not isfile(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + thumb):
				import Image
				imi = Image.open(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + im)
				imi.thumbnail((120, 120))
				imi.save(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + thumb)
			text = text.replace(i['tag'], THUMB % (domain, im, domain, thumb, im))
	return text
def art(dic, text):
	"""
	display a link to Content entry by given slug
	"""
	now = datetime.now()
	red = now - timedelta(hours=48)
	yellow = now - timedelta(hours=96)
	green = now - timedelta(hours=192)
	lista = []
	for i in dic:
		lista.append(i['attributes']['slug'])
	pages = Content.objects.filter(slug__in=lista)
	for i in pages:
		if i.date > red:
			text = text.replace('[rk:art slug="' + i.slug + '"]', '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + ' <img src="/site_media/layout/cbc/new_1.gif" alt="" /><br />')
		elif i.date > yellow:
			text = text.replace('[rk:art slug="' + i.slug + '"]', '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + ' <img src="/site_media/layout/cbc/new_3.gif" alt="" /><br />')
		elif i.date > green:
			text = text.replace('[rk:art slug="' + i.slug + '"]', '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + ' <img src="/site_media/layout/cbc/new_7.gif" alt="" / alt="" /><br />')
		else:
			text = text.replace('[rk:art slug="' + i.slug + '"]', '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + '<br />')
	return text

def h(dic, text):
	"""
	display h1-4 tags with toc support
	"""
	s = 1
	for i in dic:
		text = text.replace(i['tag'], '<a name="' + str(s) +'" class="' +  i['attributes']['id'] + '" title="' + i['code'] + '"></a><h' + i['attributes']['id'] + ' class="pageh"><a href="#' + str(s) +'">' + i['code'] + '</a></h' + i['attributes']['id'] + '>')
		s = s+1
	return text
def link(dic, text):
	"""
	display external links
	"""
	for i in dic:
		if i['attributes'].has_key('src'):
			i['attributes']['href'] = i['attributes']['src']
		if i['attributes'].has_key('desc'):
			text = text.replace(i['tag'], '<img src="/site_media/layout/cbc/browser.png" alt="" /> <a href="' + i['attributes']['href'] + '" target="_blank">' + i['code'] + '</a> - '+ i['attributes']['desc'] + '<br />')
		else:
			text = text.replace(i['tag'], '<img src="/site_media/layout/cbc/browser.png" alt="" /> <a href="' + i['attributes']['href'] + '" target="_blank">' + i['code'] + '</a><br />')
	return text
def syntax(dic, text):
	"""
	highlight code using pygments
	"""
	pygments_formatter = HtmlFormatter()
	langs = {}
	for i in dic:
		try:
			lexer = get_lexer_by_name(i['attributes']['lang'])
		except ValueError:
			lexer = get_lexer_by_name('text')
		parsed = highlight(i['code'], lexer, pygments_formatter)
		text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:11px;">' + parsed + '</div>')
		langs['<style>' + pygments_formatter.get_style_defs() + '</style>'] = True
	
	styles = ''
	for style in langs.keys():
		styles = styles + style
	text = text + styles
	return text