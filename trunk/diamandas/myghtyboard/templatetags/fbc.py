from re import findall, MULTILINE
import base64
from django import template
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

register = template.Library()

def fbc(value): # Only one argument.
	value = value.replace(':omg:', '<img src="/site_media/wiki/smilies/icon_eek.gif" alt="" />')
	value = value.replace(':nice:', '<img src="/site_media/wiki/smilies/icon_biggrin.gif" alt="" />')
	value = value.replace(':whatthe:', '<img src="/site_media/wiki/smilies/icon_neutral.gif" alt="" />')
	value = value.replace(':evil:', '<img src="/site_media/wiki/smilies/icon_evil.gif" alt="" />')
	value = value.replace(':twisted:', '<img src="/site_media/wiki/smilies/icon_twisted.gif" alt="" />')
	value = value.replace(':?:', '<img src="/site_media/wiki/smilies/icon_question.gif" alt="" />')
	value = value.replace(':idea:', '<img src="/site_media/wiki/smilies/icon_idea.gif" alt="" />')
	value = value.replace(':arrow:', '<img src="/site_media/wiki/smilies/icon_arrow.gif" alt="" />')
	value = value.replace(':grin:', '<img src="/site_media/wiki/smilies/icon_cheesygrin.gif" alt="" />')
	value = value.replace(':cool:', '<img src="/site_media/wiki/smilies/icon_cool.gif" alt="" />')
	value = value.replace('[b]', '<b>')
	value = value.replace('[/b]', '</b>')
	value = value.replace('[i]', '<i>')
	value = value.replace('[/i]', '</i>')
	value = value.replace('[u]', '<u>')
	value = value.replace('[/u]', '</u>')
	value = value.replace('[quote]', '<blockquote>')
	value = value.replace('[/quote]', '</blockquote>')
	
	value = value.replace('\n', '<br />')
	tags = findall( r'(?xs)\[code\](.*?)\[/code]''', value, MULTILINE)
	for i in tags:
		if i.find(' ') == -1:
			code = base64.decodestring(i)
		else:
			code = i
		value = value.replace('[code]' + i + '[/code]', highlight(code, HtmlLexer(), HtmlFormatter()))
	del tags
	tags = findall( r'\[url=(.*?)\](.*?)\[/url\]', value)
	for i in tags:
		if len(i) == 2:
			value = value.replace('[url='+ i[0] +']'+i[1]+'[/url]', '<a href="' + i[0] +'" target="_blank">' + i[1] +'</a>')
	del tags
	tags = findall( r'\[url\](.*?)\[/url\]', value)
	for i in tags:
		value = value.replace('[url]'+i+'[/url]', '<a href="' + i +'" target="_blank">' + i +'</a>')
	del tags
	tags = findall( r'http://([a-z_0-9=\?.&/_\-]*) ', value)
	for i in tags:
		value = value.replace('http://' + i, '<a href="http://' + i +'" target="_blank">' + i +'</a>')
	return value
register.filter('fbc', fbc)