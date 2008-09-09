#!/usr/bin/python
# Diamanda Application Set
# User Panel

from random import choice
from datetime import timedelta
from datetime import datetime
import sha

import django.contrib.auth.views
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.mail import send_mail

from django import forms
from django.contrib.auth import authenticate, login

from diamandas.userpanel.models import *
from diamandas.userpanel.context import userpanel as userpanelContext
from diamandas.userpanel.captcha import *
from diamandas.utils import *


def user_panel(request):
	"""
	main user panel
	"""
	# get associated OpenIDs if any
	o = False
	if request.user.is_authenticated():
		o = OpenIdAssociation.objects.filter(user=request.user)
		if o.count() < 1:
			o = False
	return render_to_response('userpanel/panel.html', {'admin_mail': settings.SITE_ADMIN_MAIL, 'o': o}, context_instance=RequestContext(request, userpanelContext(request)))

@login_required
def remove_openid(request, oid):
	"""
	remove associated OpenID
	"""
	try:
		o = OpenIdAssociation.objects.get(user=request.user, id=oid)
	except:
		return redirect_by_template(request, "/user/", _('Bad OpenID ID.'))
	else:
		o.delete()
		return redirect_by_template(request, "/user/", _('OpenID removed from list.'))

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
	token = forms.CharField()
	email = forms.EmailField()
	def clean(self):
		# check the answer
		if 'token' in self.cleaned_data and 'reply' in self.cleaned_data:
			try:
				ct = CaptchaToken.objects.get(token=self.cleaned_data['token'])
			except:
				raise forms.ValidationError(_("Incorrect answer."))
			else:
				now = datetime.now()
				check_time = now - timedelta(minutes=5)
				if ct.date < check_time:
					raise forms.ValidationError(_("Incorrect answer."))
				if not ct.answer == sha.new(self.cleaned_data['reply']+settings.SECRET_KEY).hexdigest():
					raise forms.ValidationError(_("Incorrect answer."))
				ct.delete()
		
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
	Quick User registration for new openIDs
	"""
	if 'new_openid' in request.session and request.session['new_openid'] == False or 'new_openid' not in request.session or request.openid == None:
		return HttpResponseRedirect("/user/")
	
	captcha = text_captcha()
	t = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(15)])
	ct = CaptchaToken(answer=captcha['answer'], token=t)
	ct.save()
	
	form =  RegisterOpenIdForm()
	if request.POST:
		stripper = Stripper()
		data = request.POST.copy()
		data['login'] = stripper.strip(data['login'])
		data['email'] = stripper.strip(data['email'])
		
		form = RegisterOpenIdForm(data)
		
		if form.is_valid():
			data = form.cleaned_data
			# a random password.
			password = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(10)])
			try:
				user = User.objects.create_user(data['login'], data['email'], password)
			except Exception:
				data['reply'] = ''
				return render_to_response(
					'userpanel/register_openid.html',
					{'token': t, 'form': form, 'question': captcha['question'], 'openid': request.openid},
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
				
				# send a email to the user with generated password
				MSG = _('You just registered on http://www.%s using OpenID') % settings.SITE_KEY
				MSG +=  ' %s.\n\r' % str(request.openid)
				MSG += _('If you will want to remove login by OpenID then you will have to use your password: %s (which can be changed after login).') % password
				send_mail(_('OpenID Registration Notification'), MSG, settings.SITE_ADMIN_MAIL, [data['email']], fail_silently=True)
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
				{'token': t, 'form': form, 'question': captcha['question'], 'openid': request.openid},
				context_instance=RequestContext(request))
	
	return render_to_response(
		'userpanel/register_openid.html',
		{'token': t, 'form': form, 'question': captcha['question'], 'openid': request.openid},
		context_instance=RequestContext(request))


class AssignOpenIdForm(forms.Form):
	"""
	Assign new OpenID to existing user account using login/password
	"""
	login = forms.CharField()
	password = forms.CharField()

def assign_openid(request):
	"""
	Assign new OpenID to existing user account using login/password
	"""
	if 'new_openid' in request.session and request.session['new_openid'] == False or 'new_openid' not in request.session or request.openid == None:
		return HttpResponseRedirect("/user/")
	
	form =  AssignOpenIdForm()
	if request.POST:
		form = AssignOpenIdForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			user = authenticate(username=data['login'], password=data['password'])
			if user is not None:
				login(request, user)
				# save the openID association
				o = OpenIdAssociation(user=user, openid=str(request.openid))
				o.save()
				request.session['new_openid'] = False
				return redirect_by_template(request, "/user/", _('OpenID assigned to your user account.'))

	return render_to_response(
		'userpanel/assign_openid.html',
		{'form': form, 'openid': request.openid},
		context_instance=RequestContext(request))

class RegisterForm(forms.Form):
	"""
	Standard registration form
	"""
	login = forms.CharField(min_length=3, max_length=30)
	password1 = forms.CharField(min_length=6)
	password2 = forms.CharField(min_length=6)
	reply = forms.CharField()
	token = forms.CharField()
	email = forms.EmailField()
	def clean(self):
		# check the answer
		if 'token' in self.cleaned_data and 'reply' in self.cleaned_data:
			try:
				ct = CaptchaToken.objects.get(token=self.cleaned_data['token'])
			except:
				raise forms.ValidationError(_("Incorrect answer."))
			else:
				now = datetime.now()
				check_time = now - timedelta(minutes=5)
				if ct.date < check_time:
					raise forms.ValidationError(_("Incorrect answer."))
				if not ct.answer == sha.new(self.cleaned_data['reply']+settings.SECRET_KEY).hexdigest():
					raise forms.ValidationError(_("Incorrect answer."))
				ct.delete()
				# remove old tokens
				ct = CaptchaToken.objects.filter(date__lte=check_time)
				for i in ct:
					i.delete()
		
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
	t = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(15)])
	ct = CaptchaToken(answer=captcha['answer'], token=t)
	ct.save()
	
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
					{'token': t, 'form': form, 'question': captcha['question'], 'error': True},
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
				{'token': t, 'form': form, 'question': captcha['question'], 'error': True},
				context_instance=RequestContext(request))
	
	return render_to_response(
		'userpanel/register.html',
		{'token': t, 'form': form, 'question': captcha['question']},
		context_instance=RequestContext(request))
