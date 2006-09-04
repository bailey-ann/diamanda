from myghtyboard.fbcparser import *
from django import template

register = template.Library()

def fbc(value): # Only one argument.
    return parse_fbc_tags(value)

register.filter('fbc', fbc)