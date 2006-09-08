import re
import sys
sys.path.append('diamandas/wiki/cbcplugins/')

def parse_cbc_tags(text):
	# lolish basic emots parser
	text = text.replace(':omg:', '<img src="/site_media/wiki/smilies/icon_eek.gif" border="0" />')
	text = text.replace(':nice:', '<img src="/site_media/wiki/smilies/icon_biggrin.gif" border="0" />')
	text = text.replace(':whatthe:', '<img src="/site_media/wiki/smilies/icon_neutral.gif" border="0" />')
	text = text.replace(':evil:', '<img src="/site_media/wiki/smilies/icon_evil.gif" border="0" />')
	text = text.replace(':twisted:', '<img src="/site_media/wiki/smilies/icon_twisted.gif" border="0" />')
	text = text.replace(':?:', '<img src="/site_media/wiki/smilies/icon_question.gif" border="0" />')
	text = text.replace(':idea:', '<img src="/site_media/wiki/smilies/icon_idea.gif" border="0" />')
	text = text.replace(':arrow:', '<img src="/site_media/wiki/smilies/icon_arrow.gif" border="0" />')
	text = text.replace(':grin:', '<img src="/site_media/wiki/smilies/icon_cheesygrin.gif" border="0" />')
	text = text.replace(':cool:', '<img src="/site_media/wiki/smilies/icon_cool.gif" border="0" />')
	
	# double: [tag]something here[/tag]
	tags = re.findall( r'(?xs)\[\s*rk:([a-z0-9]*)\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:(\1)\s*\]''', text, re.MULTILINE)
	parsed_double = {}
	for tag in tags:
		k = str(tag[0]).strip()
		v = tag[1]
		v = v.split(' ')
		vals = {}
		vals['attributes'] = {}
		for attr in v:
			attr = attr.split('=')
			val = attr[1]
			attr[1] = val[1:-1]
			vals['attributes'][attr[0]] = attr[1]
		vals['code'] = tag[2]
		vals['tag'] = '[rk:' + tag[0] + ' ' + tag[1] + ']' + tag[2] + '[/rk:' + tag[0] + ']'
		if not parsed_double.has_key(k):
			parsed_double[k] = list()
		parsed_double[k].append(vals)
	
	for plugin in parsed_double:
		try:
			exec 'from ' + plugin + ' import *'
		except:
			pass
		else:
			try:
				text = render(parsed_double[plugin], text)
			except:
				pass
			
	if text.find('[toc]') != -1:
		tags = re.findall('<a name="([0-9]*)" h="([0-9]*)" title="(.*?)"></a>', text)
		toc = ''
		for i in tags:
			pad = str((int(i[1]) -1)*20)
			toc = toc+'<div style="padding-left:' + pad + 'px; padding-bottom:3px;"><img src="/site_media/wiki/img/' + i[1] + '.png" border="0"> <a href="#' + i[0] + '">' + i[2] + '</a></div>'
		text = text.replace('[toc]', toc)
		
		
	# single: [tag]
	tags = re.findall('\[rk:([a-z0-9]*) ([a-zA-z0-9 /=.,"\']*)\]', text)
	parsed = {}
	for tag in tags:
		k = str(tag[0]).strip()
		v = tag[1]
		v = v.split(' ')
		vals = {}
		vals['attributes'] = {}
		for attr in v:
			attr = attr.split('=')
			val = attr[1]
			attr[1] = val[1:-1]
			vals['attributes'][attr[0]] = attr[1]
		vals['tag'] = '[rk:' + tag[0] + ' ' + tag[1] + ']'
		if not parsed.has_key(k):
			parsed[k] = list()
		parsed[k].append(vals)
	
	for plugin in parsed:
		try:
			exec 'from ' + plugin + ' import *'
		except:
			pass
		else:
			try:
				text = render(parsed[plugin], text)
			except:
				pass
	return text
