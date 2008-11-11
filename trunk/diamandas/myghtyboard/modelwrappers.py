#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
# add / edit posts and topics
from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.db.models import Q
from django.core.mail import mail_admins
from django.contrib.auth.decorators import login_required

from diamandas.myghtyboard.models import *
from diamandas.myghtyboard import permshelpers
from diamandas.myghtyboard.context import forum as forumContext
from diamandas.utils import *

class AddTopicForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea)
	nick = forms.CharField(required=False, initial=_('Anonymous'))
	class Meta:
		model = Topic

def add_topic(request, forum_id, inject_post=False, inject_title=False, redirect_link=False, content_obj=False):
	"""
	add topic
	
	* forum_id - ID of a Forum entry
	* inject_post - optional aditional first post text that can be injected
	* inject_title - optional topic title
	* redirect_link - optional list with 2 elements (URL, message) for redirect_by_template after topic creation
	* content_obj - optional Content object that uses topic for comments
	"""
	request.forum_id = forum_id
	perm = permshelpers.cant_add_topic(request)
	if perm:
		return perm
	
	forum = Forum.objects.get(id=forum_id)
	
	pr = False
	if forum.use_prefixes:
		p = Prefix.objects.filter(forums=forum)
		if len(p) > 0:
			pr = []
			for i in p:
				pr.append(i)
	
	if request.POST:
		stripper = Stripper()
		page_data = request.POST.copy()
		text = page_data['text']
		# block anonymous messages with multiple links
		perms = forumContext(request)
		if not perms['perms']['is_authenticated'] and text.count('http') > 1:
			return render_to_response('pages/bug.html',
				{'bug': _('To many links. Is this spam?.')},
				context_instance=RequestContext(request, perms)
				)
		if 'prefix[]' in page_data:
			prefixes = page_data.getlist("prefix[]")
			pr = Prefix.objects.filter(id__in=prefixes)
			page_data['prefixes'] = ''
			for p in pr:
				page_data['prefixes'] = '%s[%s] ' % (page_data['prefixes'], p.name)
			
			del page_data['prefix[]']
		if inject_title:
			page_data['name'] = stripper.strip(inject_title)
			page_data['is_external'] = True
		else:
			page_data['name'] = stripper.strip(page_data['name'])
		page_data['forum'] = forum_id
		page_data['posts'] = 1
		if perms['perms']['is_authenticated']:
			page_data['lastposter'] = str(request.user)
			page_data['author'] = str(request.user)
			author = str(request.user)
			page_data['author_system'] = request.user.id
		else:
			if 'nick' in page_data and len(stripper.strip(page_data['nick'])) > 2:
				author = stripper.strip(page_data['nick'])[0:14]
				page_data['lastposter'] = author
				page_data['author'] = author
				page_data['author_anonymous'] = 1
			else:
				page_data['lastposter'] = _('Anonymous')
				page_data['author'] = _('Anonymous')
				author = _('Anonymous')
				page_data['author_anonymous'] = 1
		page_data['last_pagination_page'] = 1
		page_data['modification_date'] = datetime.now()
		form = AddTopicForm(page_data)
		if form.is_valid():
			new_place = form.save()
			if 'prefixes' in page_data:
				tp = TopicPrefix(topic=new_place)
				tp.save()
				tp.prefix=pr
				tp.save()
			if inject_post:
				post = Post(topic = new_place, text = inject_post, author = author, ip = request.META['REMOTE_ADDR'])
				if 'author_anonymous' in page_data:
					post.author_anonymous = True
				post.save()
			post = Post(topic = new_place, text = text, author = author, ip = request.META['REMOTE_ADDR'])
			if 'author_anonymous' in page_data:
				post.author_anonymous = True
			else:
				post.author_system = request.user
			post.save()
			
			if content_obj:
				content_obj.coment_topic = new_place
				content_obj.save()
			
			forum.topics = forum.topics +1
			forum.posts = forum.posts +1
			forum.lastposter = author
			if len(new_place.name) > 25:
				tname = new_place.name[0:25] + '...'
			else:
				tname = new_place.name
			forum.lasttopic = '<a href="/forum/topic/1/' + str(new_place.id) + '/">' + tname + '</a>'
			forum.modification_date = datetime.now()
			forum.save()
			if settings.NOTIFY_ADMINS:
				mail_admins(_('Topic Added'), _('Topic added') + ' %s/forum/forum/%s/' % (settings.SITE_DOMAIN, forum_id), fail_silently=True)
			
			if redirect_link and len(redirect_link) == 2:
				return redirect_by_template(request, redirect_link[0], redirect_link[1])
			else:
				return redirect_by_template(request, "/forum/forum/" + forum_id +"/", _('Topic added succesfuly.'))
		else:
			return render_to_response(
				'myghtyboard/add_topic.html',
				{'form': form, 'forum': forum, 'pr': pr},
				context_instance=RequestContext(request, forumContext(request)))

	form = AddTopicForm()
	return render_to_response(
		'myghtyboard/add_topic.html',
		{'form': form, 'forum': forum, 'pr': pr},
		context_instance=RequestContext(request, forumContext(request)))

class AddPostForm(forms.ModelForm):
	nick = forms.CharField(required=False, initial=_('Anonymous'))
	class Meta:
		model = Post

def add_post(request, topic_id, post_id = False, redirect_link=False, content_obj=False):
	"""
	add post
	
	* topic_id - id of a Topic entry
	* post_id - id of a Post entry to be quoted
	* redirect_link - optional list with 2 elements (URL, message) for redirect_by_template after topic creation
	* content_obj - optional Content object that uses topic for comments
	"""
	topic = Topic.objects.get(id=topic_id)
	forum = Forum.objects.get(id=topic.forum.id)
	
	request.forum_id = forum.id
	perm = permshelpers.cant_add_post(request, topic.is_locked)
	if perm:
		return perm
	
	try:
		# check who made the last post.
		lastpost = Post.objects.order_by('-date').filter(topic=topic_id)[:2]
		# if the last poster is the current one (login) and he isn't staff then we don't let him post after his post (third post)
		if str(lastpost[0].author) == str(request.user) and str(lastpost[1].author) == str(request.user) and not is_staff:
			return render_to_response('pages/bug.html',
				{'bug': _('You can\'t post after your post')},
				context_instance=RequestContext(request, forumContext(request))
				)
	except:
		pass
	
	lastpost = Post.objects.filter(topic=topic_id).order_by('-id')[:10]
	if request.POST:
		stripper = Stripper()
		page_data = request.POST.copy()
		# block anonymous messages with multiple links
		perms = forumContext(request)
		if not perms['perms']['is_authenticated'] and page_data['text'].count('http') > 1:
			return render_to_response('pages/bug.html',
				{'bug': _('To many links. Is this spam?.')},
				context_instance=RequestContext(request, perms)
				)
		if perms['perms']['is_authenticated']:
			page_data['author'] = str(request.user)
			author = str(request.user)
			page_data['author_system'] = request.user.id
		else:
			if 'nick' in page_data and len(stripper.strip(page_data['nick'])) > 2:
				author = stripper.strip(page_data['nick'])[0:14]
				page_data['author'] = author
				page_data['author_anonymous'] = 1
			else:
				page_data['author'] = _('Anonymous')
				author = _('Anonymous')
				page_data['author_anonymous'] = 1
		page_data['ip'] = request.META['REMOTE_ADDR']
		page_data['topic'] = topic_id
		page_data['date'] = datetime.now()
		form = AddPostForm(page_data)
		if form.is_valid():
			form.save()
		
			posts = Post.objects.filter(topic=topic_id).count()
			
			pmax =  posts/10
			pmaxten =  posts%10
			if pmaxten != 0:
				pmax = pmax+1
				topic.last_pagination_page = pmax
			elif pmax > 0:
				topic.last_pagination_page = pmax
			else:
				pmax = 1
				topic.last_pagination_page = 1
			topic.posts = posts
			topic.lastposter = author
			topic.modification_date = datetime.now()
			topic.save()
			
			forum.posts = forum.posts +1
			forum.lastposter = author
			
			if len(topic.name) > 25:
				tname = topic.name[0:25] + '...'
			else:
				tname = topic.name
			forum.lasttopic = '<a href="/forum/topic/' + str(pmax) + '/' + str(topic.id) + '/">' + tname + '</a>'
			forum.modification_date = datetime.now()
			forum.save()
			
			if settings.NOTIFY_ADMINS:
				mail_admins(
					_('Post Added'),
					_('Post Added') + ' %s/forum/topic/%s/%s/' % (settings.SITE_DOMAIN, str(pmax), topic_id),
					fail_silently=True
					)
			if content_obj:
				content_obj.save()
			if redirect_link and len(redirect_link) == 2:
				return redirect_by_template(request, redirect_link[0], redirect_link[1])
			else:
				return redirect_by_template(request, "/forum/topic/" + str(pmax) + "/" + topic_id +"/", _('Post added succesfuly.'))
		else:
			return render_to_response(
				'myghtyboard/add_post.html',
				{'forum': forum, 'topic': topic, 'lastpost': lastpost, 'form':form},
				context_instance=RequestContext(request, forumContext(request)))
	else:
		if post_id:
			quote = Post.objects.get(id=post_id)
			quote_text = '[quote][b]' + quote.author + _(' wrote') + ':[/b]\n\r' + quote.text + '[/quote]\n\r'
		else:
			quote_text = ''
	form = AddPostForm()
	return render_to_response(
		'myghtyboard/add_post.html',
		{'forum': forum, 'topic': topic, 'quote_text': quote_text, 'lastpost': lastpost, 'form':form},
		context_instance=RequestContext(request, forumContext(request)))

def edit_post(request, post_id):
	"""
	edit post
	
	* post_id - id of a Post entry
	"""
	
	post = Post.objects.get(id=post_id)
	topic = Topic.objects.get(id=post.topic.id)
	forum = Forum.objects.get(id=topic.forum.id)
	request.forum_id = forum.id
	perm = permshelpers.cant_edit_post(request, topic.is_locked, post.author)
	if perm:
		return perm
	
	if request.POST and len(request.POST.copy()['text']) > 1:
		page_data = request.POST.copy()
		post.text = page_data['text']
		post.save()
		
		pmax = Post.objects.filter(topic=post.topic).count()/10
		pmaxten =  Post.objects.filter(topic=post.topic).count()%10
		if pmaxten != 0:
			pmax = pmax+1
		return redirect_by_template(request, "/forum/topic/" + str(pmax) + "/" + str(post.topic.id) +"/", _('Post edited succesfuly.'))
	else:
		return render_to_response(
			'myghtyboard/edit_post.html',
			{'forum': forum, 'topic': topic, 'text': post.text, 'post_id': post_id},
			context_instance=RequestContext(request, forumContext(request)))
