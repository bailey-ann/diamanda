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

from django import newforms as forms
from django.contrib.auth import authenticate, login
from django.core import validators

from userpanel.models import *
from userpanel.context import userpanel as userpanelContext
from utils import *
from captcha import *


def user_panel(request):
	"""
	main user panel
	"""
	return render_to_response('userpanel/panel.html', {'admin_mail': settings.SITE_ADMIN_MAIL}, context_instance=RequestContext(request, userpanelContext(request)))

def login_user(request):
	"""
	django.contrib.auth.views.login login view
	"""
	if not request.user.is_authenticated():
		# if the view is called by Ajax- Facebox then show the light version
		if 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
			return django.contrib.auth.views.login(request, template_name='userpanel/login_light.html')
		else:
			return django.contrib.auth.views.login(request, template_name='userpanel/login.html')
	else:
		return HttpResponseRedirect("/user/")

def logout_then_login(request):
	"""
	django.contrib.auth.views.logout_then_login logout view
	"""
	# logout openIDs if any
	if 'openids' in request.session:
		request.session['openids'] = []
	return django.contrib.auth.views.logout_then_login(request, login_url = '/')

@login_required
def password_change(request):
	"""
	django.contrib.auth.views.password_change password change view
	"""
	return django.contrib.auth.views.password_change(request, template_name='userpanel/password_change.html')

@login_required
def password_change_done(request):
	"""
	django.contrib.auth.views.password_change_done after password change view
	"""
	return django.contrib.auth.views.password_change_done(request, template_name='userpanel/password_change_done.html')

def password_reset(request):
	"""
	django.contrib.auth.views.password_reset view (forgotten password)
	"""
	if not request.user.is_authenticated():
		return django.contrib.auth.views.password_reset(request, template_name='userpanel/password_reset.html', email_template_name= 'userpanel/password_reset_email.html')
	else:
		return HttpResponseRedirect("/user/")

def password_reset_done(request):
	"""
	django.contrib.auth.views.password_reset_done - after password reset view
	"""
	if not request.user.is_authenticated():
		return django.contrib.auth.views.password_reset_done(request, template_name='userpanel/password_reset_done.html')
	else:
		return HttpResponseRedirect("/user/")


class RegisterOpenIdForm(forms.Form):
	"""
	Quick registration form for OpenID users
	"""
	login = forms.CharField(min_length=3, max_length=30)
	reply = forms.CharField()
	answer = forms.CharField()
	email = forms.EmailField()
	def clean(self):
		# check the answer
		if 'answer' in self.cleaned_data and 'reply' in self.cleaned_data and not self.cleaned_data['answer'] == sha.new(self.cleaned_data['reply']+settings.SECRET_KEY).hexdigest():
			raise forms.ValidationError(_("Incorrect answer."))
		# check if login is free
		try:
			User.objects.get(username=self.cleaned_data['login'])
		except:
			pass
		else:
			raise forms.ValidationError(_("Login already taken"))
		# check if email isn't used already
		try:
			User.objects.get(email=self.cleaned_data['email'])
		except:
			pass
		else:
			raise forms.ValidationError(_("Email already taken"))
		
		return self.cleaned_data

def register_from_openid(request):
	"""
	Create user based on used OpenID
	"""
	if 'new_openid' in request.session and request.session['new_openid'] == False or 'new_openid' not in request.session or request.openid == None:
		return HttpResponseRedirect("/user/")
	
	captcha = text_captcha()
	form =  RegisterOpenIdForm()
	if request.POST:
		stripper = Stripper()
		data = request.POST.copy()
		data['login'] = stripper.strip(data['login'])
		data['email'] = stripper.strip(data['email'])
		
		form = RegisterOpenIdForm(data)
		
		if form.is_valid():
			data = form.cleaned_data
			password = ''.join([choice('qwertyuiopasdfghjklzxcvbnm') for i in range(10)])
			try:
				user = User.objects.create_user(data['login'], data['email'], password)
			except Exception:
				data['reply'] = ''
				return render_to_response(
					'userpanel/register_openid.html',
					{'hash': captcha['answer'], 'form': form, 'question': captcha['question'], 'openid': request.openid},
					context_instance=RequestContext(request))
			else:
				user.save()
				user = authenticate(username=data['login'], password=password)
				if user is not None:
					login(request, user)
					# save the openID association
					o = OpenIdAssociation(user=user, openid=str(request.openid))
					o.save()
					request.session['new_openid'] = False
				return redirect_by_template(request, "/user/", _('Registration compleated. To login on this site use your OpenID. You have been logged in succesfuly.'))
		else:
			data['reply'] = ''
			# newforms are bad... ;)
			if '__all__' in form.errors:
				if str(form.errors['__all__']).find(_('Incorrect answer')) != -1:
					form.errors['reply'] = [_('Incorrect answer'),]
				if str(form.errors['__all__']).find(_("Login already taken")) != -1:
					form.errors['login'] = [_("Login already taken"),]
				if str(form.errors['__all__']).find(_("Email already taken")) != -1:
					form.errors['email'] = [_("Email already taken"),]
			return render_to_response(
				'userpanel/register_openid.html',
				{'hash': captcha['answer'], 'form': form, 'question': captcha['question'], 'openid': request.openid},
				context_instance=RequestContext(request))
	
	return render_to_response(
		'userpanel/register_openid.html',
		{'hash': captcha['answer'], 'form': form, 'question': captcha['question'], 'openid': request.openid},
		context_instance=RequestContext(request))


class RegisterForm(forms.Form):
	"""
	Standard registration form
	"""
	login = forms.CharField(min_length=3, max_length=30)
	password1 = forms.CharField(min_length=6)
	password2 = forms.CharField(min_length=6)
	reply = forms.CharField()
	answer = forms.CharField()
	email = forms.EmailField()
	def clean(self):
		# check the answer
		if 'answer' in self.cleaned_data and 'reply' in self.cleaned_data and not self.cleaned_data['answer'] == sha.new(self.cleaned_data['reply']+settings.SECRET_KEY).hexdigest():
			raise forms.ValidationError(_("Incorrect answer."))
		# check if passwords match
		if 'password2' in self.cleaned_data and 'password1' in self.cleaned_data and self.cleaned_data['password2'] != self.cleaned_data['password1'] :
			raise forms.ValidationError(_("Passwords do not match."))
		# check if login is free
		try:
			User.objects.get(username=self.cleaned_data['login'])
		except:
			pass
		else:
			raise forms.ValidationError(_("Login already taken"))
		# check if email isn't used already
		try:
			User.objects.get(email=self.cleaned_data['email'])
		except:
			pass
		else:
			raise forms.ValidationError(_("Email already taken"))
		
		return self.cleaned_data

def register(request):
	"""
	User registration
	"""
	captcha = text_captcha()
	form =  RegisterForm()
	if request.POST:
		stripper = Stripper()
		data = request.POST.copy()
		data['login'] = stripper.strip(data['login'])
		data['email'] = stripper.strip(data['email'])
		
		form = RegisterForm(data)
		
		if form.is_valid():
			data = form.cleaned_data
			try:
				user = User.objects.create_user(data['login'], data['email'], data['password1'])
			except Exception:
				data['reply'] = ''
				return render_to_response(
					'userpanel/register.html',
					{'hash': captcha['answer'], 'form': form, 'question': captcha['question'], 'error': True},
					context_instance=RequestContext(request))
			else:
				user.save()
				user = authenticate(username=data['login'], password=data['password1'])
				if user is not None:
					login(request, user)
				return redirect_by_template(request, "/user/", _('Registration compleated. You have been logged in succesfuly.'))
		else:
			data['reply'] = ''
			# newforms are bad... ;)
			if '__all__' in form.errors:
				if str(form.errors['__all__']).find(_('Incorrect answer')) != -1:
					form.errors['reply'] = [_('Incorrect answer'),]
				if str(form.errors['__all__']).find(_("Login already taken")) != -1:
					form.errors['login'] = [_("Login already taken"),]
				if str(form.errors['__all__']).find(_("Email already taken")) != -1:
					form.errors['email'] = [_("Email already taken"),]
				if str(form.errors['__all__']).find(_("Passwords do not match.")) != -1:
					form.errors['password1'] = [_("Passwords do not match."),]
			return render_to_response(
				'userpanel/register.html',
				{'hash': captcha['answer'], 'form': form, 'question': captcha['question'], 'error': True},
				context_instance=RequestContext(request))
	
	return render_to_response(
		'userpanel/register.html',
		{'hash': captcha['answer'], 'form': form, 'question': captcha['question']},
		context_instance=RequestContext(request))
