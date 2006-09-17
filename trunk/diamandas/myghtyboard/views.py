from django.shortcuts import render_to_response
from myghtyboard.models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from stripogram import html2safehtml
from django.db.models import Q
#############
# lepsza walidacja forumularzy
# paginacja tematow
############
# list permissions used in templates
def list_perms(request):
	perms = {}
	if request.user.is_authenticated() and request.user.has_perm('myghtyboard.add_topic') or settings.ANONYMOUS_CAN_ADD_TOPIC and not request.user.is_authenticated():
		perms['add_topic'] = True
	else:
		perms['add_topic'] = False
	if request.user.is_authenticated() and request.user.has_perm('myghtyboard.add_post') or settings.ANONYMOUS_CAN_ADD_POST and not request.user.is_authenticated():
		perms['add_post'] = True
	else:
		perms['add_post'] = False
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			perms['is_staff'] = True
		else:
			perms['is_staff'] = False
	else:
		perms['is_staff'] = False
	if request.user.is_authenticated():
		perms['is_authenticated'] = True
	return perms

# show all categories and their topics
def category_list(request):
	categories = Category.objects.all().order_by('cat_order')
	for c in categories:
		c.forums = c.forum_set.all().order_by('forum_order')
	
	return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/category_list.html', {'categories': categories, 'perms': list_perms(request), 'lang': settings.MYGHTYBOARD_LANG})

# list of topics in a forum
def topic_list(request, forum_id):
	#topics = Topic.objects.order_by('-topic_modification_date').filter(topic_forum=forum_id)
	topics = Topic.objects.order_by('-is_global', '-is_sticky', '-topic_modification_date').filter(Q(topic_forum=forum_id) | Q(is_global='1'))
	for i in topics:
		pmax =  i.post_set.all().count()/10
		pmaxten =  i.post_set.all().count()%10
		if pmaxten != 0:
			i.pagination_max = pmax+1
		else:
			i.pagination_max = pmax
	if topics and topics[0]:
		forum_name = topics[0].topic_forum.forum_name
	else:
		forum_name = Forum.objects.get(id=forum_id)
		forum_name = forum_name.forum_name
	return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/topics_list.html', {'topics': topics, 'forum': forum_id,  'perms': list_perms(request), 'forum_name': forum_name, 'lang': settings.MYGHTYBOARD_LANG})


# list my topics
def my_topic_list(request):
	if request.user.is_authenticated():
		topics = Topic.objects.order_by('-topic_modification_date').filter(topic_author=str(request.user))[:50]
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		forum_name = _('My Topics')
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/mytopics_list.html', {'topics': topics, 'forum_name': forum_name, 'lang': settings.MYGHTYBOARD_LANG})
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t logged in')}) # can't add topic


# list last active topics
def last_topic_list(request):
	if request.user.is_authenticated():
		topics = Topic.objects.order_by('-topic_modification_date')[:50]
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		forum_name = _('My Topics')
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/mytopics_list.html', {'topics': topics, 'forum_name': forum_name, 'lang': settings.MYGHTYBOARD_LANG})
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t logged in')}) # can't add topic


# list topics with my posts
def my_posttopic_list(request):
	if request.user.is_authenticated():
		try:
			topics = Post.objects.order_by('-post_date').filter(post_author=str(request.user)).values('post_topic').distinct()[:50]
			posts = []
			for i in topics:
				posts.append(int(i['post_topic']))
			topics = Topic.objects.order_by('-topic_modification_date').filter(id__in=posts)
			for i in topics:
				pmax =  i.post_set.all().count()/10
				pmaxten =  i.post_set.all().count()%10
				if pmaxten != 0:
					i.pagination_max = pmax+1
				else:
					i.pagination_max = pmax
			forum_name = _('My Topics')
		except:
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/mytopics_list.html', {'lang': settings.MYGHTYBOARD_LANG})
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/mytopics_list.html', {'topics': topics, 'forum_name': forum_name, 'lang': settings.MYGHTYBOARD_LANG})
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t logged in')}) # can't add topic


# list post in topic with a generic pagination view :)
def post_list(request, topic_id, pagination_id):
	from django.views.generic.list_detail import object_list
	topic = Topic.objects.get(id=topic_id)
	if  topic.is_locked:
		opened = False
	else:
		opened = True
	return object_list(request, topic.post_set.all().order_by('post_date'), paginate_by = 10, page = pagination_id, extra_context = {'topic_id':topic_id, 'opened': opened, 'lang': settings.MYGHTYBOARD_LANG, 'topic': topic.topic_name, 'forum_id': topic.topic_forum.id, 'forum_name': topic.topic_forum, 'perms': list_perms(request), 'current_user': str(request.user)}, template_name = 'myghtyboard/' + settings.MYGHTYBOARD_THEME + '/post_list.html')

# add topic
def add_topic(request, forum_id):
	# can add_topic or anonymous ANONYMOUS_CAN_ADD_TOPIC
	if request.user.is_authenticated() and request.user.has_perm('myghtyboard.add_topic') or settings.ANONYMOUS_CAN_ADD_TOPIC and not request.user.is_authenticated():
		manipulator = Topic.AddManipulator()
		if request.POST and len(request.POST.copy()['text']) > 1 and  len(request.POST.copy()['topic_name']) > 1:
			page_data = request.POST.copy()
			page_data['topic_author'] = str(request.user)
			
			import re
			import base64
			from datetime import datetime
			tags = re.findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['text'], re.MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[code]'+i+'[/code]', '[code]'+base64.b64encode(i)+'[/code]')
			page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
			text = page_data['text']
			del page_data['text']
			page_data['topic_forum'] = forum_id
			page_data['topic_posts'] = 1
			page_data['topic_lastpost'] = str(request.user)+'<br />' + str(datetime.today())[:-7]
			manipulator.do_html2python(page_data)
			new_place = manipulator.save(page_data)
			if len(request.META['REMOTE_HOST']) < 1:
				request.META['REMOTE_HOST'] = 'Unknown'
			post = Post(post_topic = new_place, post_text = text, post_author = str(request.user), post_ip = request.META['REMOTE_ADDR'], post_host = request.META['REMOTE_HOST'])
			post.save()
			forum = Forum.objects.get(id=forum_id)
			forum.forum_topics = forum.forum_topics +1
			forum.forum_posts = forum.forum_posts +1
			forum.forum_lastpost = str(request.user)+'<br />' + str(datetime.today())[:-7] + '<br /><a href="/forum/topic/1/' + str(new_place.id) + '/">' + str(new_place.topic_name) + '</a>'
			forum.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			errors = {}
			page_data = {}
		
		form = forms.FormWrapper(manipulator, page_data, errors)
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/add_topic.html', {'form': form, 'lang': settings.MYGHTYBOARD_LANG, 'perms': list_perms(request)})
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You can\'t add topics')}) # can't add topic


# add post
def add_post(request, topic_id, post_id = False):
	# can add_post or anonymous ANONYMOUS_CAN_ADD_POST
	if request.user.is_authenticated() and request.user.has_perm('myghtyboard.add_post') or settings.ANONYMOUS_CAN_ADD_POST and not request.user.is_authenticated():
		topic = Topic.objects.values('is_locked').get(id=topic_id)
		if topic['is_locked']:
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('Topic is closed')}) # locked topic!
		# check who made the last post.
		lastpost = Post.objects.order_by('-post_date').filter(post_topic=topic_id)[:1]
		if request.user.is_authenticated():
			user_data = User.objects.get(username=str(request.user))
			is_staff = user_data.is_staff
		else:
			is_staff = False
		# if the last poster is the current one (login) and he isn't staff then we don't let him post after his post
		if str(lastpost[0].post_author) == str(request.user) and not is_staff:
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You can\'t post after your post')}) # can't post after post!
		else:
			manipulator = Post.AddManipulator()
			if request.POST and len(request.POST.copy()['post_text']) > 1:
				page_data = request.POST.copy()
				page_data['post_author'] = str(request.user)
				
				import re
				import base64
				tags = re.findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], re.MULTILINE)
				from datetime import datetime
				for i in tags:
					page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.b64encode(i)+'[/code]')
				page_data['post_text'] = html2safehtml(page_data['post_text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
				
				page_data['post_ip'] = request.META['REMOTE_ADDR']
				if len(request.META['REMOTE_HOST']) < 1:
					request.META['REMOTE_HOST'] = 'Unknown'
				page_data['post_host'] = request.META['REMOTE_HOST']
				page_data['post_topic'] = topic_id
				manipulator.do_html2python(page_data)
				new_place = manipulator.save(page_data)
				
				topic = Topic.objects.get(id=topic_id)
				topic.topic_posts = topic.topic_posts +1
				topic.topic_lastpost = str(request.user)+'<br />' + str(datetime.today())[:-7]
				topic.save()
				
				forum = Forum.objects.get(id=topic.topic_forum.id)
				forum.forum_posts = forum.forum_posts +1
				
				pmax = Post.objects.filter(post_topic=topic_id).count()/10
				pmaxten =  Post.objects.filter(post_topic=topic_id).count()%10
				if pmaxten != 0:
					pmax = pmax+1
				
				forum.forum_lastpost = str(request.user)+'<br />' + str(datetime.today())[:-7] + '<br /><a href="/forum/topic/' + str(pmax) + '/' + str(topic.id) + '/">' + str(topic.topic_name) + '</a>'
				forum.save()
				
				return HttpResponseRedirect("/forum/topic/" + str(pmax) + "/" + topic_id +"/")
			else:
				if post_id:
					quote = Post.objects.get(id=post_id)
					# decode rk:source code
					import re
					import base64
					tags = re.findall( r'(?xs)\[code\](.*?)\[/code\]''', quote.post_text, re.MULTILINE)
					for i in tags:
						quote.post_text = quote.post_text.replace('[code]'+i+'[/code]', '[code]'+base64.b64decode(i)+'[/code]')
					quote_text = '<blockquote><b>' + quote.post_author + ' wrote:</b><br /><cite>' + quote.post_text + '</cite></blockquote>\n'
				else:
					quote_text = ''
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/add_post.html', {'quote_text': quote_text, 'lang': settings.MYGHTYBOARD_LANG})
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You can\'t add posts')}) # can't add posts

#edit post
def edit_post(request, post_id):
	post = Post.objects.get(id=post_id)
	topic = Topic.objects.values('is_locked').get(id=post.post_topic.id)
	if topic['is_locked']:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('Topic is closed')}) # locked topic!
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		is_staff = user_data.is_staff
	else:
		is_staff = False

	# if the editor is the post author or is he a staff member
	if str(request.user) == post.post_author and request.user.is_authenticated() or  is_staff:
		if request.POST and len(request.POST.copy()['post_text']) > 1:
			page_data = request.POST.copy()
			
			import re
			import base64
			tags = re.findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], re.MULTILINE)
			from datetime import datetime
			for i in tags:
				page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.b64encode(i)+'[/code]')
			page_data['post_text'] = html2safehtml(page_data['post_text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
			
			post.post_text = page_data['post_text']
			post.save()
			
			pmax = Post.objects.filter(post_topic=post.post_topic).count()/10
			pmaxten =  Post.objects.filter(post_topic=post.post_topic).count()%10
			if pmaxten != 0:
				pmax = pmax+1
			
			return HttpResponseRedirect("/forum/topic/" + str(pmax) + "/" + str(post.post_topic.id) +"/")
		else:
			# decode rk:source code
			import re
			import base64
			tags = re.findall( r'(?xs)\[code\](.*?)\[/code\]''', post.post_text, re.MULTILINE)
			for i in tags:
				post.post_text = post.post_text.replace('[code]'+i+'[/code]', '[code]'+base64.b64decode(i)+'[/code]')
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/edit_post.html', {'post_text': post.post_text, 'lang': settings.MYGHTYBOARD_LANG})
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You can\'t edit this post')}) # can't edit post

# delete a post
def delete_post(request, post_id, topic_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			Post.objects.get(id=post_id).delete()
			return HttpResponseRedirect("/forum/topic/1/" + topic_id +"/")
		else:
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator')}) # can't delete
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't delete

# delete a topic with all posts
def delete_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			Topic.objects.get(id=topic_id).delete()
			Post.objects.filter(id=topic_id).delete()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator')}) # can't delete
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't delete

# close topic
def close_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			topic = Topic.objects.get(id=topic_id)
			topic.is_locked=True
			topic.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator')}) # can't close
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't close
# open topic
def open_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			topic = Topic.objects.get(id=topic_id)
			topic.is_locked=False
			topic.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator')}) # can't open
	else:
		return render_to_response('myghtyboard/' + settings.MYGHTYBOARD_THEME + '/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't open