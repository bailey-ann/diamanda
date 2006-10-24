from re import findall, MULTILINE
import base64
from django import template
from pygments import highlight
from pygments.lexers import PythonLexer
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
	value = value.replace('\n', '<br />')
	tags = findall( r'(?xs)\[code\](.*?)\[/code]''', value, MULTILINE)
	for i in tags:
		code = base64.b64decode(i)
		value = value.replace('[code]' + i + '[/code]', highlight(code, PythonLexer(), HtmlFormatter(linenos=True)))
	return value
register.filter('fbc', fbc)