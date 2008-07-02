#!/usr/bin/python
# Diamanda Application Set
# CBCParhaser - replace tags with some content

from re import findall
from tags import *
import markdown
import base64

def parse_cbc_tags(text, use_mdk=True):
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
		try:
			text = eval(plugin + '(parsed_double[plugin], text)')
		except:
			print 'NO PLUGIN %s' % plugin

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
		try:
			text = eval(plugin + '(parsed[plugin], text)')
		except:
			print 'NO PLUGIN %s' % plugin
	
	#if use_mdk:
		#text = markdown.markdown(text, safe_mode = True)
	tags = findall(r'\^\^(.*?)\^\^', text)
	for tag in tags:
		text = text.replace('^^%s^^' % tag, base64.b64decode(tag))
	return text