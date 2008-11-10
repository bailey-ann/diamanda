#!/usr/bin/python
# Diamanda Application Set
# Pages module
from diamandas.cbcplugins import cbcparser
from django import template

register = template.Library()

def cbc(value):
	if value:
		return cbcparser.parse_cbc_tags(value)
	else:
		return u''

register.filter('cbc', cbc)