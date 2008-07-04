#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import newforms as forms
from django.conf import settings
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.db.models import Q
from django.core.mail import mail_admins
from django.contrib.auth.decorators import login_required

from myghtyboard.models import *
from myghtyboard.context import forum as forumContext
from utils import *

def category_list(request):
	"""
	show all categories and their topics
	"""
	categories = Category.objects.all().order_by('order')
	for c in categories:
		#{% if forum.mods %}<u>{% trans "Moderators" %}</u>:
		#        {% for i in forum.mods %}
		#               {{ i.username }}{% if not forloop.last %},{% endif %} 
		#        {% endfor %}
		#{% endif %}
		#forum = c.forum_set.all().order_by('order')
		#forums = []
		#for f in forum:
		#	f.mods = f.moderators.all()
		#	forums.append(f)
		c.forums = c.forum_set.all().order_by('order')
	return render_to_response(
		'myghtyboard/category_list.html',
		{'categories': categories},
		context_instance=RequestContext(request, forumContext(request)))


def topic_list(request, forum_id, pagination_id=1):
	"""
	list of topics in a forum
	
	* forum_id - id of a Forum record
	"""
	prefixes = False
	prefixes_list = False
	if request.POST:
		prefixes = request.POST.copy()
		prefixes = prefixes.getlist("prefix[]")
		prefixes = Prefix.objects.filter(id__in=prefixes)

	try:
		if prefixes and len(prefixes) > 0:
			tops = TopicPrefix.objects.all().values('topic').distinct()
			for i in prefixes:
				tops = tops.filter(prefix=i)
			topics_ids = []
			for tid in tops:
				topics_ids.append(tid['topic'])
			topics = Topic.objects.order_by('-is_global', '-is_sticky', '-modification_date').filter(Q(forum=forum_id) | Q(is_global='1'))
			topics = topics.filter(id__in=topics_ids)
	
		else:
			topics = Topic.objects.order_by('-is_global', '-is_sticky', '-modification_date').filter(Q(forum=forum_id) | Q(is_global='1'))

		count = topics.count()
		count = count/10
		cnt = [1]
		i = 1
		while i <= count:
			i = i+1
			cnt.append(i)
		forum = Forum.objects.get(id=forum_id)
		name = forum.name
	except:
		return redirect_by_template(request, "/forum/", _('There is no such forum. Please go back to the forum list.'))
	form = AddTopicForm()
	
	pr = False
	if forum.use_prefixes:
		p = Prefix.objects.filter(forums=forum)
		if len(p) > 0:
			pr = []
			for i in p:
				pr.append(i)
	request.forum_id = forum_id
	return object_list(
		request,
		topics,
		paginate_by = 10,
		allow_empty = True,
		page = pagination_id,
		context_processors = [forumContext],
		extra_context = {'forum': forum, 'form': form, 'current_user': str(request.user), 'pr': pr, 'prefixes': prefixes, 'cnt': cnt},
		template_name = 'myghtyboard/topics_list.html')

@login_required
def my_topic_list(request, show_user=False):
	"""
	list my topics
	
	* show_user - if not set will show current user topics
	"""
	if not show_user:
		show_user = str(request.user)
	topics = Topic.objects.order_by('-modification_date').filter(author=show_user)[:50]
	name = _('User Topics')
	return render_to_response(
		'myghtyboard/mytopics_list.html',
		{'topics': topics, 'name': name},
		context_instance=RequestContext(request, forumContext(request)))

@login_required
def last_topic_list(request):
	"""
	 list last active topics
	"""
	topics = Topic.objects.order_by('-modification_date')[:50]
	for i in topics:
		pmax =  i.post_set.all().count()/10
		pmaxten =  i.post_set.all().count()%10
		if pmaxten != 0:
			i.pagination_max = pmax+1
		else:
			i.pagination_max = pmax
	name = _('Last Active Topics')
	return render_to_response(
		'myghtyboard/mytopics_list.html',
		{'topics': topics, 'name': name},
		context_instance=RequestContext(request, forumContext(request)))

@login_required
def my_posttopic_list(request, show_user=False):
	"""
	list topics with my posts
	
	* show_user - if not set will show current user topics
	"""
	if not show_user:
		show_user = str(request.user)
	try:
		topics = Post.objects.order_by('-date').filter(author=show_user).values('topic').distinct()[:50]
		posts = []
		for i in topics:
			posts.append(int(i['topic']))
		topics = Topic.objects.order_by('-modification_date').filter(id__in=posts)
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		name = _('User Posts in Latest Topics')
	except:
		return render_to_response('myghtyboard/mytopics_list.html', {}, context_instance=RequestContext(request, forumContext(request)))
	return render_to_response(
		'myghtyboard/mytopics_list.html',
		{'topics': topics, 'name': name},
		context_instance=RequestContext(request, forumContext(request)))


def post_list(request, topic_id, pagination_id):
	"""
	 list post in topic with a generic pagination view
	
	* topic_id - id of a Topic entry
	"""
	try:
		topic = Topic.objects.get(id=topic_id)
	except Topic.DoesNotExist:
		return HttpResponseRedirect('/forum/')
	if  topic.is_locked:
		opened = False
	else:
		opened = True
	if topic.author_anonymous == False and request.user == topic.author_system:
		is_author = True
	else:
		is_author = False
	forum = topic.forum
	request.forum_id = forum.id
	form = AddPostForm()
	return object_list(
		request,
		topic.post_set.all().order_by('date'),
		paginate_by = 10,
		page = pagination_id,
		context_processors = [forumContext],
		extra_context = {
			'opened': opened,
			'is_author': is_author,
			'topic': topic,
			'forum_id': forum.id,
			'form': form,
			'forum_name': forum,
			'current_user': str(request.user)},
		template_name = 'myghtyboard/post_list.html')

class AddTopicForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea)
	nick = forms.CharField(required=False, initial=_('Anonymous'))
	class Meta:
		model = Topic

def add_topic(request, forum_id):
	"""
	add topic
	
	* forum_id - ID of a Forum entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	if not perms['perms']['add_topic'] and not perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t add a topic.')},
			context_instance=RequestContext(request, forumContext(request))
			)
	if not perms['perms']['add_topic'] and perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('To many anonymous posts. Login to post topics and new messages.')},
			context_instance=RequestContext(request, forumContext(request))
			)
	
	forum = Forum.objects.get(id=forum_id)
	
	lasttopic = Topic.objects.filter(forum=forum).order_by('-modification_date')[:3]
	if str(lasttopic[0].author) == str(request.user) and str(lasttopic[1].author) == str(request.user) and str(lasttopic[2].author) == str(request.user) and not perms['perms']['is_staff'] \
	or lasttopic[0].author_anonymous and lasttopic[1].author_anonymous and lasttopic[2].author_anonymous:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t make more than 3 topics in a row')},
			context_instance=RequestContext(request, forumContext(request))
			)
	
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
		if not perms['perms']['is_authenticated'] and text.count('http') > 1:
			return render_to_response('pages/bug.html',
				{'bug': _('To many links. Is this spam?.')},
				context_instance=RequestContext(request, forumContext(request))
				)
		if 'prefix[]' in page_data:
			prefixes = page_data.getlist("prefix[]")
			pr = Prefix.objects.filter(id__in=prefixes)
			page_data['prefixes'] = ''
			for p in pr:
				page_data['prefixes'] = '%s[%s] ' % (page_data['prefixes'], p.name)
			
			del page_data['prefix[]']
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
			
			post = Post(topic = new_place, text = text, author = author, ip = request.META['REMOTE_ADDR'])
			if 'author_anonymous' in page_data:
				post.author_anonymous = True
			else:
				post.author_system = request.user
			post.save()
			
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
				mail_admins(_('Topic Added'), _('Topic added') + ' http://www.%s/forum/forum/%s/' % (settings.SITE_KEY, id), fail_silently=True)
			
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

def add_post(request, topic_id, post_id = False):
	"""
	add post
	
	* topic_id - id of a Topic entry
	* post_id - id of a Post entry to be quoted
	"""
	topic = Topic.objects.get(id=topic_id)
	forum = Forum.objects.get(id=topic.forum.id)
	
	request.forum_id = forum.id
	perms = forumContext(request)
	if not perms['perms']['add_post'] and not perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t add a post.')},
			context_instance=RequestContext(request, forumContext(request))
			)
	if not perms['perms']['add_post'] and perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('To many anonymous posts. Login to post topics and new messages.')},
			context_instance=RequestContext(request, forumContext(request))
			)
	
	if topic.is_locked:
		return render_to_response('pages/bug.html', {'bug': _('Topic is closed')}, context_instance=RequestContext(request, forumContext(request)))

	# check who made the last post.
	lastpost = Post.objects.order_by('-date').filter(topic=topic_id)[:1]
	# if the last poster is the current one (login) and he isn't staff then we don't let him post after his post
	if str(lastpost[0].author) == str(request.user) and not is_staff or str(lastpost[0].ip) == str(request.META['REMOTE_ADDR']) and not perms['perms']['is_staff']:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t post after your post')},
			context_instance=RequestContext(request, forumContext(request))
			)
	
	lastpost = Post.objects.filter(topic=topic_id).order_by('-id')[:10]
	if request.POST:
		stripper = Stripper()
		page_data = request.POST.copy()
		# block anonymous messages with multiple links
		if not perms['perms']['is_authenticated'] and page_data['text'].count('http') > 1:
			return render_to_response('pages/bug.html',
				{'bug': _('To many links. Is this spam?.')},
				context_instance=RequestContext(request, forumContext(request))
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
					_('Post Added') + ' http://www.%s/forum/topic/%s/%s/' % (settings.SITE_KEY, str(pmax), topic_id),
					fail_silently=True
					)
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
	perms = forumContext(request)
	if not perms['perms']['add_post'] and str(request.user) != post.author:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t edit a post.')},
			context_instance=RequestContext(request, forumContext(request))
			)

	if topic.is_locked:
		return render_to_response('pages/bug.html',
			{'bug': _('Topic is closed')},
			context_instance=RequestContext(request, forumContext(request))
			)
	
	if str(request.user) == post.author or perms['perms']['is_staff']:
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
	else:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t edit this post')},
			context_instance=RequestContext(request, forumContext(request))
			)


def delete_post(request, post_id, topic_id):
	"""
	delete a post
	
	* post_id - ID of a Post entry
	* topic_id - Topic entry ID that contain the Post entry
	"""
	topic = Topic.objects.get(id=topic_id)
	request.forum_id = topic.forum.id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		Post.objects.get(id=post_id).delete()
		topic.posts = topic.posts -1
		if topic.posts > 0:
			topic.save()
			return redirect_by_template(request, "/forum/topic/1/" + topic_id +"/", _('Post deleted succesfuly.'))
		else:
			fid = topic.forum.id
			topic.delete()
			return redirect_by_template(request, "/forum/forum/%s/" % fid, _('Topic deleted succesfuly.'))
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request, forumContext(request)))


def delete_topic(request, topic_id, forum_id):
	"""
	delete a topic with all posts
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		posts = Post.objects.filter(topic=topic_id).count()
		t = Topic.objects.get(id=topic_id)
		if t.forum.id != forum_id:
			return render_to_response('pages/bug.html', {'bug': _('Invalid Forum/Topic')}, context_instance=RequestContext(request, forumContext(request)))
		t.delete()
		Post.objects.filter(topic=topic_id).delete()
		forum = Forum.objects.get(id=forum_id)
		forum.topics = forum.topics -1
		forum.posts = forum.posts - posts
		forum.save()
		return redirect_by_template(request, "/forum/forum/" + forum_id +"/", _('Topic deleted succesfuly.'))
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request, forumContext(request)))


def move_topic(request, topic_id, forum_id):
	"""
	move topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		if request.POST and len(request.POST['forum']) > 0:
			topic = Topic.objects.get(id=topic_id)
			topic.forum=Forum.objects.get(id=request.POST['forum'])
			topic.save()
			t = Topic(
				forum=Forum.objects.get(id=forum_id),
				name = topic.name,
				author = topic.author,
				posts = 0,
				lastposter = _('Topic Moved'),
				is_locked = True)
			t.save()
			p = Post(
				topic = t,
				text = _('This topic has been moved to another forum. To see the topic follow')
					 + ' <a href="/forum/topic/1/' + str(topic_id) +'/"><b>' + _('this link') + '</b></a>',
				author = _('Forum Staff'),
				ip = str(request.META['REMOTE_ADDR']))
			p.save()
			return redirect_by_template(request, "/forum/forum/" + forum_id +"/", _('Topic moved succesfuly.'))
		else:
			forums = Forum.objects.exclude(id=forum_id)
			topic = Topic.objects.get(id=topic_id)
			return render_to_response(
				'myghtyboard/move_topic.html',
				{'forums': forums, 'topic': topic},
				context_instance=RequestContext(request, forumContext(request)))
	else:
		return render_to_response('pages/bug.html',
			{'bug': _('You aren\'t a moderator')},
			context_instance=RequestContext(request, forumContext(request))
			)


def close_topic(request, topic_id, forum_id):
	"""
	close topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		topic = Topic.objects.get(id=topic_id)
		topic.is_locked=True
		topic.save()
		return redirect_by_template(request, "/forum/forum/" + forum_id +"/", _('Topic closed succesfuly.'))
	else:
		return render_to_response('pages/bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request, forumContext(request)))


def open_topic(request, topic_id, forum_id):
	"""
	open topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		topic = Topic.objects.get(id=topic_id)
		topic.is_locked=False
		topic.save()
		return redirect_by_template(request, "/forum/forum/" + forum_id +"/", _('Topic opened succesfuly.'))
	else:
		return render_to_response('pages/bug.html',
			{'bug': _('You aren\'t a moderator and you aren\'t logged in')},
			context_instance=RequestContext(request, forumContext(request))
			)

def solve_topic(request, topic_id, forum_id):
	"""
	marks topic as solved
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	topic = Topic.objects.get(id=topic_id)
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff'] or perms['perms']['is_authenticated'] and topic.author == str(request.user):
		topic.is_solved=True
		topic.save()
		return redirect_by_template(request, "/forum/forum/" + forum_id +"/", _('Topic solved.'))
	else:
		return render_to_response('pages/bug.html',
			{'bug': _('You aren\'t a moderator or topic author and you aren\'t logged in')},
			context_instance=RequestContext(request, forumContext(request))
			)

def unsolve_topic(request, topic_id, forum_id):
	"""
	marks topic as unsolved
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	topic = Topic.objects.get(id=topic_id)
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff'] or perms['perms']['is_authenticated'] and topic.author == str(request.user):
		topic.is_solved=False
		topic.save()
		return redirect_by_template(request, "/forum/forum/" + forum_id +"/", _('Topic unsolved.'))
	else:
		return render_to_response('pages/bug.html',
			{'bug': _('You aren\'t a moderator or topic author and you aren\'t logged in')},
			context_instance=RequestContext(request, forumContext(request))
			)
