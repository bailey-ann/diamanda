#!/usr/bin/python
# Diamanda Application Set
# Boxcomments - global comment system

from random import choice
import Image, ImageDraw, ImageFont, sha
from stripogram import html2safehtml

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django import newforms as forms
from django.utils.translation import ugettext as _
from django.core.mail import mail_admins

from boxcomments.models import *
from pages.models import Content
from translator.models import Translation


class CommentForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	imgtext = forms.CharField()
	author = forms.CharField(required=False)
	imghash = forms.CharField(widget=forms.HiddenInput)
	def clean(self):
		SALT = settings.SECRET_KEY[:20]
		if not 'imgtext' in self.cleaned_data or not self.cleaned_data['imghash'] == sha.new(SALT+self.cleaned_data['imgtext'].upper()).hexdigest():
			raise forms.ValidationError('Captha Error')
		return self.cleaned_data

def comments(request, apptype, appid, quoteid=False):
	"""
	Show and add comments to defined object
	
	*apptype - application
	*appid - ID of an app record
	"""
	# create a 5 char random strin and sha hash it
	imgtext = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(5)])
	SALT = settings.SECRET_KEY[:20]
	imghash = sha.new(SALT+imgtext).hexdigest()
	# create an image with the string
	im=Image.open(settings.MEDIA_ROOT + '/bg.jpg')
	draw=ImageDraw.Draw(im)
	font=ImageFont.truetype(settings.MEDIA_ROOT + '/SHERWOOD.TTF', 26)
	draw.text((5,5),imgtext, font=font, fill=(100,100,50))
	im.save(settings.MEDIA_ROOT + '/captcha/' + str(request.user) + '.jpg',"JPEG")
	
	com = Comment.objects.filter(apptype= apptype, appid = appid).order_by('id')[:20]
	if len(com)>=2 and com[0].ip == com[1].ip and com[0].ip == request.META['REMOTE_ADDR']:
		ban = True
	else:
		ban = False
	try:
		if apptype == '1':
			a = Content.objects.get(id = appid)
			title = a.title
		elif apptype == '4':
			a = Translation.objects.get(id = appid)
			title = a.name
	except:
		return render_to_response('pages/bug.html', {'bug': _('No such entry')}, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if request.user.is_authenticated():
				author = str(request.user)
			elif 'author' in data.keys() and len(data['author']) > 1:
				author = html2safehtml(data['author'] ,valid_tags=())
			else:
				author = _('Anonymous User')
			text = html2safehtml(data['text'] ,valid_tags=())
			co = Comment(title = title,appid = appid, text = text, author = author, ip = request.META['REMOTE_ADDR'], apptype = apptype)
			co.save()
			if apptype == '1':
				a.comments_count = a.comments_count + 1
				a.save()
			if settings.NOTIFY_ADMINS:
				mail_admins(_('Comment added'), _('A Comment have been added on: http://www.') + settings.SITE_KEY, fail_silently=True)
			return HttpResponseRedirect('/com/' + str(appid) + '/' + str(apptype) + '/')
		else:
			if str(form.errors).find('Captha Error') >= 0:
				if not 'imgtext' in form.errors:
					form.errors['imgtext'] = []
				form.errors['imgtext'].append(_('Captcha Error'))
			return render_to_response(
				'boxcomments/comments.html',
				{'hash': imghash, 'form': form, 'com': com, 'appid': appid, 'apptype': apptype, 'a': a, 'ban': ban, 'title':title},
				context_instance=RequestContext(request))

	if quoteid:
		q = Comment.objects.get(id=quoteid)
		form =  CommentForm({'text':'[quote][b]@' + q.author + '[/b]\n' + q.text + '[/quote]\n\n'})
	else:
		form =  CommentForm()

	return render_to_response(
		'boxcomments/comments.html',
		{'hash': imghash, 'form': form, 'com': com, 'appid': appid, 'apptype': apptype, 'a': a, 'ban': ban, 'title':title},
		context_instance=RequestContext(request))