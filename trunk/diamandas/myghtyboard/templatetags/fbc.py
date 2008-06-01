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
	return value

register.filter('fbc', fbc)
