from re import findall
from os.path import isfile
from os import listdir

def list_descriptions():
	plugins = listdir('/home/piotr/svn/bib/diamandas/cbcplugins/cbcplugins')
	plug = {}
	for p in plugins:
		plug[p.split('.')[0]] = True
	plugins = plug.keys()
	descriptions = []
	for plugin in plugins:
		if plugin.isalpha():
			exec 'from ' + plugin + ' import *'
			descriptions.append(describe())
	return descriptions

def parse_cbc_tags(text):
	list_descriptions()
	# lolish basic emots parser
	text = text.replace(':omg:', '<img src="/site_media/wiki/smilies/icon_eek.gif" alt="" />')
	text = text.replace(':nice:', '<img src="/site_media/wiki/smilies/icon_biggrin.gif" alt="" />')
	text = text.replace(':whatthe:', '<img src="/site_media/wiki/smilies/icon_neutral.gif" alt="" />')
	text = text.replace(':evil:', '<img src="/site_media/wiki/smilies/icon_evil.gif" alt="" />')
	text = text.replace(':twisted:', '<img src="/site_media/wiki/smilies/icon_twisted.gif" alt="" />')
	text = text.replace(':?:', '<img src="/site_media/wiki/smilies/icon_question.gif" alt="" />')
	text = text.replace(':idea:', '<img src="/site_media/wiki/smilies/icon_idea.gif" alt="" />')
	text = text.replace(':arrow:', '<img src="/site_media/wiki/smilies/icon_arrow.gif" alt="" />')
	text = text.replace(':grin:', '<img src="/site_media/wiki/smilies/icon_cheesygrin.gif" alt="" />')
	text = text.replace(':cool:', '<img src="/site_media/wiki/smilies/icon_cool.gif" alt="" />')
	
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
		if isfile('/home/piotr/svn/bib/diamandas/cbcplugins/cbcplugins/' + plugin + '.py'):
			#try:
			exec 'from ' + plugin + ' import *'
			text = render(parsed_double[plugin], text)
			#except:
			#print 'CBC Error: ' + str(plugin)
			
	if text.find('[toc]') != -1:
		tags = findall('<a name="([0-9]*)" href="([0-9]*)" title="(.*?)"></a>', text)
		toc = ''
		for i in tags:
			pad = str((int(i[1]) -1)*20)
			toc = toc+'<div style="padding-left:' + pad + 'px; padding-bottom:3px;"><img src="/site_media/wiki/img/' + i[1] + '.png" alt="" /> <a href="#' + i[0] + '">' + i[2] + '</a></div>'
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
		if isfile('/home/piotr/svn/bib/diamandas/cbcplugins/cbcplugins/' + plugin + '.py'):
			#try:
			exec 'from ' + plugin + ' import *'
			text = render(parsed[plugin], text)
			#except:
			#print 'CBC Error: ' + str(plugin)
	return text