from wiki.cbcparser import *
from django import template

register = template.Library()

def cbc(value): # Only one argument.
    return parse_cbc_tags(value)

register.filter('cbc', cbc)