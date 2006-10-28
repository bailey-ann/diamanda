from django.shortcuts import render_to_response
from myghtyboard.models import *
from userpanel.models import *
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from stripogram import html2safehtml
from django.db.models import Q
from django.core import validators

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
	perms['css_theme'] = settings.CSS_THEME
	return perms

# show all categories and their topics
def category_list(request):
	categories = Category.objects.all().order_by('cat_order')
	for c in categories:
		c.forums = c.forum_set.all().order_by('forum_order')
	
	return render_to_response('myghtyboard/category_list.html', {'categories': categories, 'perms': list_perms(request)})

# list of topics in a forum
def topic_list(request, forum_id):
	topics = Topic.objects.order_by('-is_global', '-is_sticky', '-topic_modification_date').filter(Q(topic_forum=forum_id) | Q(is_global='1'))
	for i in topics:
		pmax =  i.post_set.all().count()/10
		pmaxten =  i.post_set.all().count()%10
		if pmaxten != 0:
			i.pagination_max = pmax+1
		else:
			i.pagination_max = pmax
	forum_name = Forum.objects.get(id=forum_id)
	forum_name = forum_name.forum_name
	return render_to_response('myghtyboard/topics_list.html', {'topics': topics, 'forum': forum_id,  'perms': list_perms(request), 'forum_name': forum_name})


# list my topics
def my_topic_list(request, show_user=False):
	if not show_user:
		show_user = str(request.user)
	if request.user.is_authenticated():
		topics = Topic.objects.order_by('-topic_modification_date').filter(topic_author=show_user)[:50]
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		forum_name = _('User Topics')
		return render_to_response('myghtyboard/mytopics_list.html', {'topics': topics, 'forum_name': forum_name})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t logged in')}) # can't add topic


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
		forum_name = _('Last Active Topics')
		return render_to_response('myghtyboard/mytopics_list.html', {'topics': topics, 'forum_name': forum_name})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t logged in')}) # can't add topic


# list topics with my posts
def my_posttopic_list(request, show_user=False):
	if not show_user:
		show_user = str(request.user)
	if request.user.is_authenticated():
		try:
			topics = Post.objects.order_by('-post_date').filter(post_author=show_user).values('post_topic').distinct()[:50]
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
			forum_name = _('User Posts in Latest Topics')
		except:
			return render_to_response('myghtyboard/mytopics_list.html', {'lang': settings.MYGHTYBOARD_LANG})
		return render_to_response('myghtyboard/mytopics_list.html', {'topics': topics, 'forum_name': forum_name})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t logged in')}) # can't add topic


# list post in topic with a generic pagination view :)
def post_list(request, topic_id, pagination_id):
	from django.views.generic.list_detail import object_list
	topic = Topic.objects.get(id=topic_id)
	if  topic.is_locked:
		opened = False
	else:
		opened = True
	if settings.FORUMS_USE_CAPTCHA:
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
		im.save(settings.SITE_IMAGES_DIR_PATH + '../bg2.jpg',"JPEG")
		return object_list(request, topic.post_set.all().order_by('post_date'), paginate_by = 10, page = pagination_id, extra_context = {'hash': imghash, 'topic_id':topic_id, 'opened': opened, 'topic': topic.topic_name, 'forum_id': topic.topic_forum.id, 'forum_name': topic.topic_forum, 'perms': list_perms(request), 'current_user': str(request.user)}, template_name = 'myghtyboard/post_list.html')
	else:
		return object_list(request, topic.post_set.all().order_by('post_date'), paginate_by = 10, page = pagination_id, extra_context = {'topic_id':topic_id, 'opened': opened, 'topic': topic.topic_name, 'forum_id': topic.topic_forum.id, 'forum_name': topic.topic_forum, 'perms': list_perms(request), 'current_user': str(request.user)}, template_name = 'myghtyboard/post_list.html')

# add topic
def add_topic(request, forum_id):
	if settings.FORUMS_USE_CAPTCHA:
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
		im.save(settings.SITE_IMAGES_DIR_PATH + '../bg2.jpg',"JPEG")
		
	# can add_topic or anonymous ANONYMOUS_CAN_ADD_TOPIC
	if request.user.is_authenticated() and request.user.has_perm('myghtyboard.add_topic') or settings.ANONYMOUS_CAN_ADD_TOPIC and not request.user.is_authenticated():
		manipulator = Topic.AddManipulator()
		if request.POST and len(request.POST.copy()['text']) > 1 and  len(request.POST.copy()['topic_name']) > 1:
			page_data = request.POST.copy()
			if settings.FORUMS_USE_CAPTCHA and page_data['imghash'] != sha.new(page_data['imgtext']).hexdigest():
				errors = {}
				page_data = {}
				form = forms.FormWrapper(manipulator, page_data, errors)
				post_text = html2safehtml(request.POST.copy()['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
				return render_to_response('myghtyboard/add_topic.html', {'form': form, 'hash': imghash, 'perms': list_perms(request), 'post_text': post_text})

			page_data['topic_author'] = str(request.user)
			from re import findall, MULTILINE
			import base64
			from datetime import datetime
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['text'], MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[code]'+i+'[/code]', '[code]'+base64.encodestring(i)+'[/code]')
			page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
			text = page_data['text']
			if request.user.is_authenticated():
				try:
					profil = Profile.objects.get(username=request.user)
				except Profile.DoesNotExist:
					pass
				else:
					if len(profil.signature) > 1:
						text = text + '<br /><br />-------------------------------------------------<br />' + profil.signature
			del page_data['text']
			page_data['topic_forum'] = forum_id
			page_data['topic_posts'] = 1
			page_data['topic_lastpost'] = str(request.user)+'<br />' + str(datetime.today())[:-7]
			manipulator.do_html2python(page_data)
			new_place = manipulator.save(page_data)
			post = Post(post_topic = new_place, post_text = text, post_author = str(request.user), post_ip = request.META['REMOTE_ADDR'])
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
		if settings.FORUMS_USE_CAPTCHA:
			return render_to_response('myghtyboard/add_topic.html', {'form': form, 'hash': imghash, 'perms': list_perms(request)})
		else:
			return render_to_response('myghtyboard/add_topic.html', {'form': form, 'perms': list_perms(request)})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t add topics')}) # can't add topic


# add post
def add_post(request, topic_id, post_id = False):
	if settings.FORUMS_USE_CAPTCHA:
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
		im.save(settings.SITE_IMAGES_DIR_PATH + '../bg2.jpg',"JPEG")
		
	# can add_post or anonymous ANONYMOUS_CAN_ADD_POST
	if request.user.is_authenticated() and request.user.has_perm('myghtyboard.add_post') or settings.ANONYMOUS_CAN_ADD_POST and not request.user.is_authenticated():
		topic = Topic.objects.values('is_locked').get(id=topic_id)
		if topic['is_locked']:
			return render_to_response('myghtyboard/noperm.html', {'why': _('Topic is closed')}) # locked topic!
		# check who made the last post.
		lastpost = Post.objects.order_by('-post_date').filter(post_topic=topic_id)[:1]
		if request.user.is_authenticated():
			user_data = User.objects.get(username=str(request.user))
			is_staff = user_data.is_staff
		else:
			is_staff = False
		# if the last poster is the current one (login) and he isn't staff then we don't let him post after his post
		if str(lastpost[0].post_author) == str(request.user) and not is_staff:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t post after your post')}) # can't post after post!
		else:
			manipulator = Post.AddManipulator()
			if request.POST and len(request.POST.copy()['post_text']) > 1:
				page_data = request.POST.copy()
				
				if settings.FORUMS_USE_CAPTCHA and page_data['imghash'] != sha.new(page_data['imgtext']).hexdigest():
					errors = {}
					page_data = {}
					form = forms.FormWrapper(manipulator, page_data, errors)
					post_text = html2safehtml(request.POST.copy()['post_text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
					return render_to_response('myghtyboard/add_post.html', {'lang': settings.MYGHTYBOARD_LANG, 'lastpost': lastpost, 'hash': imghash, 'post_text': post_text})

				
				page_data['post_author'] = str(request.user)
				if request.user.is_authenticated():
					try:
						profil = Profile.objects.get(username=request.user)
					except Profile.DoesNotExist:
						pass
					else:
						if len(profil.signature) > 3:
							page_data['post_text'] = page_data['post_text'] + '<br /><br />-------------------------------------------------<br />' + profil.signature
				from re import findall, MULTILINE
				import base64
				tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], MULTILINE)
				from datetime import datetime
				for i in tags:
					page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.encodestring(i)+'[/code]')
				page_data['post_text'] = html2safehtml(page_data['post_text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
				
				page_data['post_ip'] = request.META['REMOTE_ADDR']
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
					from re import findall, MULTILINE
					import base64
					tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', quote.post_text, MULTILINE)
					for i in tags:
						quote.post_text = quote.post_text.replace('[code]'+i+'[/code]', '[code]'+base64.decodestring(i)+'[/code]')
					quote_text = '<blockquote><b>' + quote.post_author + ' wrote:</b><br /><cite>' + quote.post_text + '</cite></blockquote>\n'
				else:
					quote_text = ''
			# get 10 last posts from this topic
			lastpost = Post.objects.filter(post_topic=topic_id).order_by('-id')[:10]
			if settings.FORUMS_USE_CAPTCHA:
				return render_to_response('myghtyboard/add_post.html', {'quote_text': quote_text, 'lastpost': lastpost, 'hash': imghash})
			else:
				return render_to_response('myghtyboard/add_post.html', {'quote_text': quote_text, 'lastpost': lastpost})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t add posts')}) # can't add posts

#edit post
def edit_post(request, post_id):
	post = Post.objects.get(id=post_id)
	topic = Topic.objects.values('is_locked').get(id=post.post_topic.id)
	if topic['is_locked']:
		return render_to_response('myghtyboard/noperm.html', {'why': _('Topic is closed')}) # locked topic!
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		is_staff = user_data.is_staff
	else:
		is_staff = False

	# if the editor is the post author or is he a staff member
	if str(request.user) == post.post_author and request.user.is_authenticated() or  is_staff:
		if request.POST and len(request.POST.copy()['post_text']) > 1:
			page_data = request.POST.copy()
			
			from re import findall, MULTILINE
			import base64
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], MULTILINE)
			from datetime import datetime
			for i in tags:
				page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.encodestring(i)+'[/code]')
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
			from re import findall, MULTILINE
			import base64
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', post.post_text, MULTILINE)
			for i in tags:
				post.post_text = post.post_text.replace('[code]'+i+'[/code]', '[code]'+base64.decodestring(i)+'[/code]')
			return render_to_response('myghtyboard/edit_post.html', {'post_text': post.post_text})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t edit this post')}) # can't edit post

# delete a post
def delete_post(request, post_id, topic_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			Post.objects.get(id=post_id).delete()
			topic = Topic.objects.get(id=topic_id)
			topic.topic_posts = topic.topic_posts -1
			topic.save()
			return HttpResponseRedirect("/forum/topic/1/" + topic_id +"/")
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator')}) # can't delete
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't delete

# delete a topic with all posts
def delete_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			posts = Post.objects.filter(post_topic=topic_id).count()
			Topic.objects.get(id=topic_id).delete()
			Post.objects.filter(post_topic=topic_id).delete()
			forum = Forum.objects.get(id=forum_id)
			forum.forum_topics = forum.forum_topics -1
			forum.forum_posts = forum.forum_posts - posts
			forum.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator')}) # can't delete
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't delete

# move topic
def move_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			if request.POST and len(request.POST['forum']) > 0:
				topic = Topic.objects.get(id=topic_id)
				topic.topic_forum=Forum.objects.get(id=request.POST['forum'])
				topic.save()
				t = Topic(topic_forum=Forum.objects.get(id=forum_id), topic_name = topic.topic_name, topic_author = topic.topic_author, topic_posts = 0, topic_lastpost = _('Topic Moved'), is_locked = True)
				t.save()
				p = Post(post_topic = t, post_text = _('This topic has been moved to another forum. To see the topic follow') + ' <a href="/forum/topic/1/' + str(topic_id) +'/"><b>' + _('this link') + '</b></a>', post_author = _('Forum Staff'), post_ip = str(request.META['REMOTE_ADDR']))
				p.save()
				return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
			else:
				forums = Forum.objects.exclude(id=forum_id).exclude(is_redirect=True)
				topic = Topic.objects.get(id=topic_id)
				return render_to_response('myghtyboard/move_topic.html', {'forums': forums, 'topic': topic})
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator')}) # can't move
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't move

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
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator')}) # can't close
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't close

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
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator')}) # can't open
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in')}) # can't open
