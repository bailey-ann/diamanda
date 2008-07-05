#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from postmarkup import render_bbcode

from django import template
from django.conf import settings

register = template.Library()

def fbc(value):
	"""
	Parse emotes, BBcode and format [code] blocks
	"""
	value = render_bbcode(value,'UTF-8')
	value = value.replace(' :( ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-unhappy.png" alt="" />')
	value = value.replace(' :o ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-surprised.png" alt="" />')
	value = value.replace(' :p ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-tongue.png" alt="" />')
	value = value.replace(' ;) ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-wink.png" alt="" />')
	value = value.replace(' :D ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-smile.png" alt="" />')
	return value

register.filter('fbc', fbc)
