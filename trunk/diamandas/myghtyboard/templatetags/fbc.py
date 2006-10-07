import re
import base64
from django import template

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
	value = value.replace('[quote]', '<blockquote>')
	value = value.replace('[/quote]', '</blockquote>')
	value = value.replace('[b]', '<b>')
	value = value.replace('[/b]', '</b>')
	value = value.replace('[u]', '<u>')
	value = value.replace('[/u]', '</u>')
	value = value.replace('[i]', '<i>')
	value = value.replace('[/i]', '</i>')
	value = value.replace('\n', '<br />')
	#dp.syntaxhighlighter 1.4.0 [code] tag
	tags = re.findall( r'(?xs)\[code\](.*?)\[/code]''', value, re.MULTILINE)
	for i in tags:
		code = base64.b64decode(i).replace('</te', '</ te')
		code = code.replace('</TE', '</ TE')
		code = code.replace('</Te', '</ Te')
		code = code.replace('</tE', '</ tE')
		value = value.replace('[code]' + i + '[/code]', '<textarea name="code" class="xml" rows="15" cols="90">' + code + '</textarea>')
	tags = re.findall( r'(?xs)\[url\](.*?)\[/url]''', value, re.MULTILINE)
	for i in tags:
		value = value.replace('[url]' + i + '[/url]', '<a href="' + i + '">' + i + '</a>')
	tags = re.findall( r'(?xs)\[url=(.*?)\](.*?)\[/url]''', value, re.MULTILINE)
	for i in tags:
		if len(i) == 2:
			value = value.replace('[url=' +i[0]+ ']' + i[1] + '[/url]', '<a href="' + i[0] + '">' + i[1] + '</a>')
	return value
register.filter('fbc', fbc)