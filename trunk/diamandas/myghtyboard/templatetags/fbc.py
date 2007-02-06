from re import findall, MULTILINE
from django import template
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter
from os.path import isfile
from django.contrib.sites.models import Site
from django.conf import settings

register = template.Library()

def fbc(value): # Only one argument.
	value = value.decode('utf-8')
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
	value = value.replace('[QUOTE]', '<blockquote>')
	value = value.replace('[url]', '')
	value = value.replace('[/url]', '')
	value = value.replace('[/URL]', '')
	value = value.replace('[URL]', '')
	
	value = value.replace('\n', '<br />')
	tags = findall( r'(?xs)\[code\](.*?)\[/code]''', value, MULTILINE)
	for i in tags:
		j = i.replace('<br />', '')
		value = value.replace('[code]' + i + '[/code]', '<div class="box" style="overflow:auto;font-size:10px;background-color:#EEEEEE;">' + highlight(j, HtmlLexer(), HtmlFormatter()) + '</div><style>' + HtmlFormatter().get_style_defs('.highlight') + '</style>')
	return value
register.filter('fbc', fbc)