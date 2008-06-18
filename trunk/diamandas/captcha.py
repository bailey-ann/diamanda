#!/usr/bin/python
# Diamanda Application Set
# textCaptcha implementation

from random import choice, randint
import sha

from django.conf import settings
from django.utils.translation import ugettext as _

def text_captcha():
	"""
	Select a random question
	and return a dictionary with question, and a sha1 hash of the correct answer
	"""
	
	# UNCOMMENT below if you want to use premade question - You have to write them
	#return logic_question()
	
	q = choice('12')
	if q == '1':
		return digit_from_number()
	elif q == '2':
		return char_from_string()

def digit_from_number():
	integer = ''.join([choice('0123456789') for i in range(4)])
	offset = int(choice('0123'))
	answer = sha.new('%s%s' % (integer[offset], settings.SECRET_KEY)).hexdigest()
	return {'question': _('What\'s the %s digit in %s?') % (offset+1, integer), 'answer': answer}

def char_from_string():
	char = ''.join([choice('qwertyuiopasdfghjklzxcvbnm') for i in range(4)])
	offset = int(choice('0123'))
	answer = sha.new('%s%s' % (char[offset], settings.SECRET_KEY)).hexdigest()
	return {'question': _('What\'s the %s character in %s?') % (offset+1, char), 'answer': answer}

def logic_question():
	"""
	Your own captcha questions
	"""
	QUESTIONS = [
		{'question': 'How much is 2+2?', 'answer': '4'},
		{'question': 'How much is 2+1?', 'answer': '3'},
		{'question': 'How much is 2+0?', 'answer': '2'},
		{'question': 'How much is 2+3?', 'answer': '5'},
		]
	index = randint(0, len(QUESTIONS) - 1)
	elem = QUESTIONS[index]
	elem['answer'] = sha.new('%s%s' % (elem['answer'], settings.SECRET_KEY)).hexdigest()
	return elem

