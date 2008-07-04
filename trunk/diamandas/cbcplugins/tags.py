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

import Image
from PIL import ImageEnhance

from django.conf import settings

def thumb(dic, text):
	"""
	display an image with a thumbnail and lightbox like script
	"""
	THUMB = '<a href="/site_media/resources/%s/images/%s" rel="facebox"><img src="/site_media/resources/%s/images/%s" alt="%s" /></a>'
	for i in dic:
		img = i['attributes']['src'].split('/')
		thumb = 'thumb_' + img[-1]
		im = img[-1]
		domain = img[0]
		if isfile(settings.MEDIA_ROOT + '/resources/' + domain + '/images/' + im):
			if not isfile(settings.MEDIA_ROOT + '/resources/' + domain + '/images/' + thumb):
				imi = Image.open(settings.MEDIA_ROOT + '/resources/' + domain + '/images/' + im)
				imi.thumbnail((145, 145), Image.ANTIALIAS)
				sharpener = ImageEnhance.Sharpness(imi)
				imi = sharpener.enhance(2.4)
				imi.save(settings.MEDIA_ROOT + '/resources/' + domain + '/images/' + thumb)
			thm = THUMB % (domain, im, domain, thumb, im)
			text = text.replace(i['tag'], thm)
	return text
def art(dic, text):
	"""
	display a link to Content entry by given slug
	"""
	from pages.models import Content
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
			text = text.replace('[rk:art slug="' + i.slug + '"]',  '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + ' <img src="/site_media/layout/cbc/new_1.gif" alt="" /><br />')
		elif i.date > yellow:
			text = text.replace('[rk:art slug="' + i.slug + '"]',  '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + ' <img src="/site_media/layout/cbc/new_3.gif" alt="" /><br />')
		elif i.date > green:
			text = text.replace('[rk:art slug="' + i.slug + '"]',  '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + ' <img src="/site_media/layout/cbc/new_7.gif" alt="" / alt="" /><br />')
		else:
			text = text.replace('[rk:art slug="' + i.slug + '"]',  '<img src="/site_media/layout/cbc/1.png" alt="" /> <a href="/w/p/' + i.slug + '/">' + i.title + '</a> - ' + i.description + '<br />')
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
		text = text.replace(i['tag'],  '<div class="box" style="overflow:hidden;font-size:11px;">' + parsed + '</div>')
		langs['<style>' + pygments_formatter.get_style_defs() + '</style>'] = True
	
	styles = ''
	for style in langs.keys():
		styles = styles + style
	text = text + styles
	return text

def box(dic, text):
	"""
	a small blue CSS box for text with a header
	"""
	TEMPLATE = '''<div class="content_float">
	<div class="content_box_header">%s</div>
	<div  class="content_box">
		%s
	</div>
	</div>'''
	
	for i in dic:
		text = text.replace(i['tag'],  TEMPLATE % (i['attributes']['title'], i['code']))
	return text
