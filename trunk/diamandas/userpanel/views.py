from django.shortcuts import render_to_response
from userpanel.models import *
from django import forms
from django.core import validators
from django.http import HttpResponseRedirect
from django.conf import settings
from stripogram import html2safehtml
from django.contrib.auth.models import User, Group
from tempfile import mkstemp
from os import remove

# main user panel
def user_panel(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/user/login/")
	return render_to_response('userpanel/' + settings.ENGINE + '/panel.html', {'current': request.user.has_perm('wiki.can_set_current'), 'add': request.user.has_perm('wiki.add_page'), 'edit': request.user.has_perm('wiki.change_page'), 'theme': settings.THEME, 'engine': settings.ENGINE})

# list of users
def userlist(request):
	users = User.objects.all()
	return render_to_response('userpanel/' + settings.ENGINE + '/userlist.html', {'users': users, 'theme': settings.THEME, 'engine': settings.ENGINE})
##################################
# Register a user and add it to default user group
##################################
class RegisterForm(forms.Manipulator):
	def __init__(self):
		self.fields = (forms.TextField(field_name="login", length=20, maxlength=200, is_required=True, validator_list=[validators.isAlphaNumeric, self.size3]),
		forms.PasswordField(field_name="password1", length=20, maxlength=200, is_required=True, validator_list=[validators.isAlphaNumeric, self.size4]),
		forms.PasswordField(field_name="password2", length=20, maxlength=200, is_required=True, validator_list=[validators.isAlphaNumeric, self.size4]),
		forms.TextField(field_name="imgtext", is_required=True, validator_list=[self.hashcheck], length=20),
		forms.TextField(field_name="imghash", is_required=True, length=20),
		forms.EmailField(field_name="email", is_required=True, length=20),)
	def hashcheck(self, field_data, all_data):
		import sha
		if not all_data['imghash'] == sha.new(field_data).hexdigest():
			raise validators.ValidationError(_("Captcha Error."))
	def size3(self, field_data, all_data):
		if len(field_data) < 4:
			raise validators.ValidationError(_("Login to short"))
	def size4(self, field_data, all_data):
		if len(field_data) < 5:
			raise validators.ValidationError(_("Password to short"))


# register user
def register(request):
	from django.contrib.auth import authenticate, login
	# captcha image creation
	from random import choice
	import Image, ImageDraw, ImageFont, sha
	temp = settings.SITE_IMAGES_DIR_PATH + request.META['REMOTE_ADDR'] + '.jpg'
	tempname = request.META['REMOTE_ADDR'] + '.jpg'
	# create a 5 char random strin and sha hash it
	imgtext = choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')
	imghash = sha.new(imgtext).hexdigest()
	# create an image with the string
	im=Image.open(settings.SITE_IMAGES_DIR_PATH + '../bg.jpg')
	draw=ImageDraw.Draw(im)
	font=ImageFont.truetype(settings.SITE_IMAGES_DIR_PATH + '../SHERWOOD.TTF', 18)
	draw.text((10,10),imgtext, font=font, fill=(100,100,50))
	im.save(temp,"JPEG")
	
	manipulator = RegisterForm()
	if request.POST:
		data = request.POST.copy()
		errors = manipulator.get_validation_errors(data)
		if not errors:
			data['email'] = html2safehtml(data['email'] ,valid_tags=())
			try:
				user = User.objects.create_user(data['login'], data['email'], data['password1'])
			except Exception:
				data['imgtext'] = ''
				form = forms.FormWrapper(manipulator, data, errors)
				return render_to_response('userpanel/' + settings.ENGINE + '/register.html', {'error': True, 'form': form, 'theme': settings.THEME, 'engine': settings.ENGINE, 'temp':tempname})
			else:
				user.save()
				user = authenticate(username=data['login'], password=data['password1'])
				if user is not None:
					login(request, user)
					user.groups.add(Group.objects.get(name='users'))
				remove(temp)
				return HttpResponseRedirect("/user/")
		else:
			data['imgtext'] = ''
			form = forms.FormWrapper(manipulator, data, errors)
			return render_to_response('userpanel/' + settings.ENGINE + '/register.html', {'error': True, 'hash': imghash, 'form': form, 'theme': settings.THEME, 'engine': settings.ENGINE, 'temp':tempname})
	else:
		errors = data = {}
	form = forms.FormWrapper(manipulator, data, errors)
	return render_to_response('userpanel/' + settings.ENGINE + '/register.html', {'hash': imghash, 'form': form, 'theme': settings.THEME, 'engine': settings.ENGINE, 'temp':tempname})

##############################################
# Login / logout user
##############################################
class LoginForm(forms.Manipulator):
	def __init__(self):
		self.fields = (forms.TextField(field_name="login", length=30, maxlength=200, is_required=True),
		forms.PasswordField(field_name="password", length=30, maxlength=200, is_required=True),
		forms.TextField(field_name="imgtext", is_required=True, validator_list=[self.hashcheck]),
		forms.TextField(field_name="imghash", is_required=True),)
	def hashcheck(self, field_data, all_data):
		import sha
		if not all_data['imghash'] == sha.new(field_data).hexdigest():
			raise validators.ValidationError("Captcha Error.")

def loginlogout(request):
	from django.contrib.auth import authenticate, login
	if not request.user.is_authenticated():
		temp = settings.SITE_IMAGES_DIR_PATH + request.META['REMOTE_ADDR'] + '.jpg'
		tempname = request.META['REMOTE_ADDR'] + '.jpg'
		# captcha image creation
		from random import choice
		import Image, ImageDraw, ImageFont, sha
		# create a 5 char random strin and sha hash it
		imgtext = choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')
		imghash = sha.new(imgtext).hexdigest()
		# create an image with the string
		im=Image.open(settings.SITE_IMAGES_DIR_PATH + '../bg.jpg')
		draw=ImageDraw.Draw(im)
		font=ImageFont.truetype(settings.SITE_IMAGES_DIR_PATH + '../SHERWOOD.TTF', 18)
		draw.text((10,10),imgtext, font=font, fill=(100,100,50))
		im.save(temp,"JPEG")
		
		manipulator = LoginForm()
		# log in user
		if request.POST:
			data = request.POST.copy()
			errors = manipulator.get_validation_errors(data)
			if not errors:
				manipulator.do_html2python(data)
				user = authenticate(username=data['login'], password=data['password'])
				if user is not None:
					login(request, user)
					remove(temp)
					#remove(settings.SITE_IMAGES_DIR_PATH + '/' + tempname)
					return HttpResponseRedirect("/user/")
				else:
					data['imgtext'] = ''
					form = forms.FormWrapper(manipulator, data, errors)
					return render_to_response('userpanel/' + settings.ENGINE + '/login.html', {'loginform': True, 'error': True, 'hash': imghash, 'form': form, 'theme': settings.THEME, 'engine': settings.ENGINE, 'temp':tempname})
		# no post data, show the login forum
		else:
			errors = data = {}
		form = forms.FormWrapper(manipulator, data, errors)
		return render_to_response('userpanel/' + settings.ENGINE + '/login.html', {'loginform': True, 'hash': imghash, 'form': form, 'theme': settings.THEME, 'engine': settings.ENGINE, 'temp':tempname})
	else:
		# user authenticated
		if request.GET:
			# logout user
			data = request.GET.copy()
			if data['log'] == 'out':
				from django.contrib.auth import logout
				logout(request)
				return HttpResponseRedirect("/user/")
		return HttpResponseRedirect("/user/")

##############################
# Send messages - emails
##############################
class PMessage(forms.Manipulator):
	def __init__(self):
		self.fields = (forms.TextField(field_name="subject", length=30, maxlength=200, is_required=True),
		forms.LargeTextField(field_name="contents", is_required=True),)

def send_pmessage(request, target_user):
	if request.user.is_authenticated() and str(request.user) != str(target_user) and len(str(target_user)) > 0 and str(target_user) != 'AnonymousUser':
		manipulator = PMessage()
		if request.POST:
			new_data = request.POST.copy()
			errors = manipulator.get_validation_errors(new_data)
			if not errors:
				manipulator.do_html2python(new_data)
				from django.core.mail import send_mail
				ruser = User.objects.get(username=str(request.user))
				send_mail(new_data['subject'], new_data['contents'], request.user.email, [ruser.email], fail_silently=True)
				return HttpResponseRedirect("/user/")
		else:
			errors = new_data = {}
		form = forms.FormWrapper(manipulator, new_data, errors)
		return render_to_response('userpanel/' + settings.ENGINE + '/pmessage.html', {'form': form, 'theme': settings.THEME, 'engine': settings.ENGINE})
	else:
		return HttpResponseRedirect("/user/")

##############################
# Profile
##############################
def edit_profile(request):
	if request.user.is_authenticated():
		try:
			p = Profile.objects.get(username=request.user)
		except:
			p = Profile(username=request.user)
			p.save()
		manipulator = Profile.ChangeManipulator(p.id)
		data = manipulator.flatten_data()
		if request.POST:
			data = request.POST.copy()
			data['username'] = request.user.id
			errors = manipulator.get_validation_errors(data)
			if not errors:
				manipulator.do_html2python(data)
				data['email'] = html2safehtml(data['email'] ,valid_tags=())
				data['signature'] = html2safehtml(data['signature'] ,valid_tags=('br', 'b', 'u', 'i', 'a'))
				data['public_info'] = html2safehtml(data['public_info'] ,valid_tags=('br', 'b', 'u', 'i', 'a'))
				data['contacts'] = html2safehtml(data['contacts'] ,valid_tags=('br', 'b', 'u', 'i', 'a'))
				manipulator.save(data)
				return HttpResponseRedirect("/user/")
		else:
			errors = {}
		form = forms.FormWrapper(manipulator, data, errors)
		return render_to_response('userpanel/' + settings.ENGINE + '/profile.html', {'theme': settings.THEME, 'engine': settings.ENGINE, 'form': form})
	else:
		return HttpResponseRedirect("/user/login/")

# show a user profile profile
def show_profile(request, show_user):
	if request.user.is_authenticated():
		try:
			profile = Profile.objects.get(username=User.objects.get(username=show_user))
		except:
			return render_to_response('userpanel/' + settings.ENGINE + '/noperm.html', {'why': _('No such profile'), 'theme': settings.THEME, 'engine': settings.ENGINE})
		return render_to_response('userpanel/' + settings.ENGINE + '/show_profile.html', {'profile': profile, 'theme': settings.THEME, 'engine': settings.ENGINE})
	else:
		return HttpResponseRedirect("/user/")
