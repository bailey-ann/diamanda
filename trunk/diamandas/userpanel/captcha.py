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
	q = _('What\'s the ') + str(offset+1) + _(' digit in %s?') % integer
	return {'question': q, 'answer': answer}

def char_from_string():
	char = ''.join([choice('qwertyuiopasdfghjklzxcvbnm') for i in range(4)])
	offset = int(choice('0123'))
	answer = sha.new('%s%s' % (char[offset], settings.SECRET_KEY)).hexdigest()
	q = _('What\'s the ') + str(offset+1) + _(' character in %s?') % char
	return {'question': q, 'answer': answer}

def logic_question():
	"""
	Your own captcha questions
	"""
	QUESTIONS = [
		{'question': 'What\'s the main color of Ferrari?', 'answer': 'red'},
		]
	index = randint(0, len(QUESTIONS) - 1)
	elem = QUESTIONS[index]
	elem['answer'] = sha.new('%s%s' % (elem['answer'], settings.SECRET_KEY)).hexdigest()
	return elem

