import re
import base64
from django import template

register = template.Library()

def fbc(value): # Only one argument.
	value = value.replace(':omg:', '<img src="/site_media/wiki/smilies/icon_eek.gif" border="0">')
	value = value.replace(':nice:', '<img src="/site_media/wiki/smilies/icon_biggrin.gif" border="0">')
	value = value.replace(':whatthe:', '<img src="/site_media/wiki/smilies/icon_neutral.gif" border="0">')
	value = value.replace(':evil:', '<img src="/site_media/wiki/smilies/icon_evil.gif" border="0">')
	value = value.replace(':twisted:', '<img src="/site_media/wiki/smilies/icon_twisted.gif" border="0">')
	value = value.replace(':?:', '<img src="/site_media/wiki/smilies/icon_question.gif" border="0">')
	value = value.replace(':idea:', '<img src="/site_media/wiki/smilies/icon_idea.gif" border="0">')
	value = value.replace(':arrow:', '<img src="/site_media/wiki/smilies/icon_arrow.gif" border="0">')
	value = value.replace(':grin:', '<img src="/site_media/wiki/smilies/icon_cheesygrin.gif" border="0">')
	value = value.replace(':cool:', '<img src="/site_media/wiki/smilies/icon_cool.gif" border="0">')
	value = value.replace('\n', '<br>')
	#dp.syntaxhighlighter 1.4.0 [code] tag
	tags = re.findall( r'(?xs)\[code\](.*?)\[/code]''', value, re.MULTILINE)
	for i in tags:
		code = base64.b64decode(i).replace('</te', '</ te')
		code = code.replace('</TE', '</ TE')
		code = code.replace('</Te', '</ Te')
		code = code.replace('</tE', '</ tE')
		value = value.replace('[code]' + i + '[/code]', '<textarea name="code" class="xml" rows="15" cols="90">' + code + '</textarea>')
	return value
register.filter('fbc', fbc)