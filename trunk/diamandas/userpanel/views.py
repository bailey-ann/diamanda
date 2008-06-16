#!/usr/bin/python
# Diamanda Application Set
# User Panel

from random import choice
import Image, ImageDraw, ImageFont, sha

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from django import oldforms as forms
from django.contrib.auth import authenticate, login
from django.core import validators

from userpanel.models import *
from userpanel.context import userpanel as userpanelContext
from utils import *



def user_panel(request):
	"""
	main user panel
	"""
	return render_to_response('userpanel/panel.html', {'admin_mail': settings.SITE_ADMIN_MAIL}, context_instance=RequestContext(request, userpanelContext(request)))

def login_user(request):
	if not request.user.is_authenticated():
		return django.contrib.auth.views.login(request, template_name='userpanel/login.html')
	else:
		return HttpResponseRedirect("/user/")

def logout_then_login(request):
	return django.contrib.auth.views.logout_then_login(request)

@login_required
def password_change(request):
	return django.contrib.auth.views.password_change(request, template_name='userpanel/password_change.html')

@login_required
def password_change_done(request):
	return django.contrib.auth.views.password_change_done(request, template_name='userpanel/password_change_done.html')

def password_reset(request):
	if not request.user.is_authenticated():
		return django.contrib.auth.views.password_reset(request, template_name='userpanel/password_reset.html', email_template_name= 'userpanel/password_reset_email.html')
	else:
		return HttpResponseRedirect("/user/")

def password_reset_done(request):
	if not request.user.is_authenticated():
		return django.contrib.auth.views.password_reset_done(request, template_name='userpanel/password_reset_done.html')
	else:
		return HttpResponseRedirect("/user/")


class RegisterForm(forms.Manipulator):
	"""
	User registration manipulator
	"""
	def __init__(self):
		self.fields = (forms.TextField(field_name="login", length=20, max_length=200, is_required=True, validator_list=[self.size3, self.freelogin]),
		forms.PasswordField(field_name="password1", length=20, max_length=200, is_required=True, validator_list=[self.size4, self.equal]),
		forms.PasswordField(field_name="password2", length=20, max_length=200, is_required=True, validator_list=[self.size4]),
		forms.TextField(field_name="imgtext", is_required=True, validator_list=[self.hashcheck], length=20),
		forms.TextField(field_name="imghash", is_required=True, length=20),
		forms.EmailField(field_name="email", is_required=True, length=20, validator_list=[self.freemail]),)
	def hashcheck(self, field_data, all_data):
		SALT = settings.SECRET_KEY[:20]
		if not all_data['imghash'] == sha.new(SALT+field_data.upper()).hexdigest():
			raise validators.ValidationError(_("Incorrect captcha text."))
	def size3(self, field_data, all_data):
		if len(field_data) < 4:
			raise validators.ValidationError(_("Login is to short"))
	def size4(self, field_data, all_data):
		if len(field_data) < 5:
			raise validators.ValidationError(_("Password is to short"))
	def equal(self, field_data, all_data):
		if all_data['password2'] != field_data:
			raise validators.ValidationError(_("Passwords do not match"))
	def freelogin(self, field_data, all_data):
		try:
			User.objects.get(username=field_data)
		except:
			pass
		else:
			raise validators.ValidationError(_("Login already taken"))
	def freemail(self, field_data, all_data):
		try:
			User.objects.get(email=field_data)
		except:
			pass
		else:
			raise validators.ValidationError(_('Email already taken'))

def register(request):
	"""
	User registration
	"""
	# create a 5 char random strin and sha hash it
	imgtext = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(5)])
	SALT = settings.SECRET_KEY[:20]
	imghash = sha.new(unicode(SALT)+unicode(imgtext)).hexdigest()
	# create an image with the string
	im=Image.open(settings.MEDIA_ROOT + '/bg.jpg')
	draw=ImageDraw.Draw(im)
	font=ImageFont.truetype(settings.MEDIA_ROOT + '/SHERWOOD.TTF', 26)
	draw.text((5,5),imgtext, font=font, fill=(100,100,50))
	im.save(settings.MEDIA_ROOT + '/captcha/' + str(request.user) + '.jpg',"JPEG")
	
	manipulator = RegisterForm()
	if request.POST:
		data = request.POST.copy()
		stripper = Stripper()
		data['login'] = stripper.strip(data['login'])
		data['email'] = stripper.strip(data['email'])
		errors = manipulator.get_validation_errors(data)
		if not errors:
			try:
				user = User.objects.create_user(data['login'], data['email'], data['password1'])
			except Exception:
				data['imgtext'] = ''
				form = forms.FormWrapper(manipulator, data, errors)
				return render_to_response(
					'userpanel/register.html',
					{'error': True, 'form': form},
					context_instance=RequestContext(request))
			else:
				user.save()
				user = authenticate(username=data['login'], password=data['password1'])
				if user is not None:
					login(request, user)
				return redirect_by_template(request, "/user/", _('Registration compleated. You have been logged in succesfuly.'))
		else:
			data['imgtext'] = ''
			form = forms.FormWrapper(manipulator, data, errors)
			return render_to_response(
				'userpanel/register.html',
				{'error': True, 'hash': imghash, 'form': form},
				context_instance=RequestContext(request))
	else:
		errors = data = {}
	form = forms.FormWrapper(manipulator, data, errors)
	return render_to_response(
		'userpanel/register.html',
		{'hash': imghash, 'form': form},
		context_instance=RequestContext(request))
