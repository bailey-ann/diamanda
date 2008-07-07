#!/usr/bin/python
# Diamanda Application Set
# Pages module
from diamandas.cbcplugins import cbcparser
from django import template

register = template.Library()

def cbc(value):
	return cbcparser.parse_cbc_tags(value)

register.filter('cbc', cbc)