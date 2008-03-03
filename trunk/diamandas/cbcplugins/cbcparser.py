#!/usr/bin/python
# Diamanda Application Set
# CBCParhaser - replace tags with some content

from re import findall
from tags import *


def parse_cbc_tags(text):
	# double: [tag]something here[/tag]
	tags = findall( r'(?xs)\[\s*rk:([a-z0-9]*)\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:(\1)\s*\]''', text)
	parsed_double = {}
	for tag in tags:
		k = str(tag[0]).strip()
		v = tag[1]
		v = v.split('" ')
		vals = {}
		vals['attributes'] = {}
		for attr in v:
			attr = attr.split('=')
			val = attr[1]
			if val[-1] != '"':
				attr[1] = val[1:]
			else:
				attr[1] = val[1:-1]
			vals['attributes'][attr[0]] = attr[1]
		vals['code'] = tag[2]
		vals['tag'] = '[rk:' + tag[0] + ' ' + tag[1] + ']' + tag[2] + '[/rk:' + tag[0] + ']'
		if not parsed_double.has_key(k):
			parsed_double[k] = list()
		parsed_double[k].append(vals)
	
	for plugin in parsed_double:
		text = eval(plugin + '(parsed_double[plugin], text)')

			
	if text.find('[toc]') != -1:
		tags = findall('<a name="([0-9]*)" class="([0-9]*)" title="(.*?)"></a>', text)
		toc = ''
		for i in tags:
			pad = str((int(i[1]) -1)*20)
			toc = toc+'<div style="padding-left:' + pad + 'px; padding-bottom:3px;"><img src="/site_media/layout/cbc/' + i[1] + '.png" alt="" /> <a href="#' + i[0] + '">' + i[2] + '</a></div>'
		text = text.replace('[toc]', toc)
		
		
	# single: [tag]
	tags = findall(r'\[rk:([a-z_0-9]*) (.*?)\]', text)
	parsed = {}
	for tag in tags:
		k = str(tag[0]).strip()
		v = tag[1]
		v = v.split('" ')
		vals = {}
		vals['attributes'] = {}
		for attr in v:
			attr = attr.split('=')
			val = attr[1]
			if val[-1] != '"':
				attr[1] = val[1:]
			else:
				attr[1] = val[1:-1]
			vals['attributes'][attr[0]] = attr[1]
		vals['tag'] = '[rk:' + tag[0] + ' ' + tag[1] + ']'
		if not parsed.has_key(k):
			parsed[k] = list()
		parsed[k].append(vals)
	
	for plugin in parsed:
		text = eval(plugin + '(parsed[plugin], text)')
	return text