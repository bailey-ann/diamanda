#!/usr/bin/python
# Diamanda Application Set
# Pages module

from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django import newforms as forms
from django.core.mail import mail_admins

from pages.models import *
from userpanel.models import Profile
from myghtyboard.models import *
from myghtyboard.context import forum as forumContext
from myghtyboard.views import AddPostForm, AddTopicForm
from utils import *

def show_index(request):
	"""
	Show the main page
	"""
	feed = Feed.objects.get(site=settings.SITE_ID)
	now = datetime.now()
	check_time = now - timedelta(minutes=10)
	onsite = Profile.objects.select_related().filter(onsitedata__gt=check_time).order_by('-onsitedata')[:4]
	try:
		p = Content.objects.get(slug='index')
	except:
		home = settings.DEFAULT_HOME_TEXT
	else:
		home = p.parsed_text
	return render_to_response(
		'pages/show_index.html',
		{'onsite': onsite, 'home_text': home, 'feed': feed},
		context_instance=RequestContext(request))

def list_news(request, book=False):
	"""
	List news
	
	* book - slug of a Content entry (book content_type)
	"""
	if book:
		bk = Content.objects.get(slug=book)
		news = Content.objects.filter(content_type='news', place=bk).order_by('-date')
		return object_list(
			request,
			news,
			paginate_by = 10,
			allow_empty = True,
			template_name = 'pages/news_list.html',
			extra_context = {'book': book, 'bk':bk, 'current_book': bk.slug})
	else:
		news = Content.objects.filter(content_type='news').order_by('-date')
	return object_list(
		request,
		news,
		paginate_by = 10,
		allow_empty = True,
		template_name = 'pages/news_list.html',
		extra_context = {'book': book})

def show(request, slug):
	"""
	show Content entry
	
	* slug - slug of a Content entry
	"""
	try:
		page = Content.objects.get(slug=slug)
	except Content.DoesNotExist:
		return render_to_response('pages/bug.html',
			{'bug': _('Page does not exist')},
			context_instance=RequestContext(request))
	
	if page.current_book:
		cb = page.current_book
	
	add_topic = False
	if page.coment_forum:
		request.forum_id = page.coment_forum.id
		coment_forum_id = page.coment_forum.id
		perms = forumContext(request)
		if perms['perms']['add_topic']:
			add_topic = True
	elif page.place and page.place.coment_forum:
		request.forum_id = page.place.coment_forum.id
		coment_forum_id = page.place.coment_forum.id
		perms = forumContext(request)
		if perms['perms']['add_topic']:
			add_topic = True
	
	if request.POST and add_topic and not page.coment_topic:
		forum = Forum.objects.get(id=coment_forum_id)
		page_data = request.POST.copy()
		page_data['author'] = str(request.user)
		text = page_data['text']
		
		page_data['name'] = _('Comments for: %s') % page.title
		page_data['forum'] = coment_forum_id
		page_data['posts'] = 1
		page_data['lastposter'] = str(request.user)
		page_data['last_pagination_page'] = 1
		page_data['is_external'] = True
		page_data['modification_date'] = datetime.now()
		form = AddTopicForm(page_data)
		if form.is_valid():
			new_place = form.save()
			COMMENT_POST = _('This is a discussion about article: [url="/w/p/%s/"]%s[/url].') % (page.slug, page.title)
			post = Post(topic = new_place, text = COMMENT_POST, author = str(request.user), ip = request.META['REMOTE_ADDR'])
			post.save()
			
			post = Post(topic = new_place, text = text, author = str(request.user), ip = request.META['REMOTE_ADDR'])
			post.save()
			
			forum.topics = forum.topics +1
			forum.posts = forum.posts +1
			forum.lastposter = str(request.user)
			if len(new_place.name) > 25:
				tname = new_place.name[0:25] + '...'
			else:
				tname = new_place.name
			forum.lasttopic = '<a href="/forum/topic/1/' + str(new_place.id) + '/">' + tname + '</a>'
			forum.modification_date = datetime.now()
			forum.save()
			
			page.coment_topic = new_place
			page.comments_count = page.coment_topic.posts
			page.save()
			
			if settings.NOTIFY_ADMINS:
				mail_admins(_('Comment Topic Created'), _('Topic added: http://www.%s/forum/forum/%s/') % (settings.SITE_KEY, coment_forum_id), fail_silently=True)
			
			return redirect_by_template(request, "/w/p/" + slug +"/?a=a", _('Comment added succesfuly.'))
	elif request.POST and add_topic and page.coment_topic:
		topic = Topic.objects.get(id=page.coment_topic.id)
		forum = Forum.objects.get(id=topic.forum.id)
		
		page_data = request.POST.copy()
		page_data['author'] = str(request.user)
		page_data['ip'] = request.META['REMOTE_ADDR']
		page_data['topic'] = page.coment_topic.id
		page_data['date'] = datetime.now()
		form = AddPostForm(page_data)
		if form.is_valid():
			form.save()
		
			posts = Post.objects.filter(topic=topic).count()
			
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
			topic.lastposter = str(request.user)
			topic.modification_date = datetime.now()
			topic.save()
			
			forum.posts = forum.posts +1
			
			forum.lastposter = str(request.user)
			if len(topic.name) > 25:
				tname = topic.name[0:25] + '...'
			else:
				tname = topic.name
			forum.lasttopic = '<a href="/forum/topic/' + str(pmax) + '/' + str(topic.id) + '/">' + tname + '</a>'
			forum.modification_date = datetime.now()
			forum.save()
			
			page.comments_count = page.coment_topic.posts
			page.save()
			
			if settings.NOTIFY_ADMINS:
				mail_admins(
					_('Comment Post Added'),
					_('Post Added: http://www.%s/forum/topic/%s/%s/') % (settings.SITE_KEY, str(pmax), topic.id),
					fail_silently=True
					)
			return redirect_by_template(request, "/w/p/" + slug +"/?a=a", _('Comment added succesfuly.'))
		
	
	if page.content_type == 'news':
		return render_to_response(
			'pages/show_news.html',
			{'page': page, 'add_topic': add_topic},
			context_instance=RequestContext(request, {'current_book': cb}))
	return render_to_response(
		'pages/show.html',
		{'page': page, 'add_topic': add_topic},
		context_instance=RequestContext(request, {'current_book': cb}))

def sitemap(request):
	"""
	Sitemap generator
	"""
	pages = Content.objects.values('slug', 'date', 'content_type')
	for p in pages:
		p['date'] = str(p['date'])[0:10]
	return render_to_response('pages/sitemap.html', {'pages': pages}, context_instance=RequestContext(request))

def full_rss(request):
	"""
	RSS channel
	"""
	pages = Content.objects.all().values('slug', 'title', 'parsed_description', 'date', 'content_type').order_by('-id')[:10]
	return render_to_response('pages/rss2.html', {'pages': pages}, context_instance=RequestContext(request))

def book_rss(request, slug):
	"""
	RSS channel for a book
	
	* book - slug of a Content entry (book content_type)
	"""
	book = Content.objects.get(slug=slug)
	pages = Content.objects.all().filter(place=book).values('slug', 'title',
		'parsed_description', 'date', 'content_type').order_by('-id')[:10]
	return render_to_response('pages/rss1.html', {'pages': pages, 'book': book}, context_instance=RequestContext(request))

#def add_comment(request, slug):
	#try:
		#page = Content.objects.filter(slug=slug).values(
			#'id', 'slug', 'date', 'title', 'parsed_description', 'description',
			#'parsed_text', 'comments_count', 'current_book', 'crumb', 'content_type')
	#except Content.DoesNotExist:
		#return render_to_response('pages/bug.html',
			#{'bug': _('Page does not exist')},
			#context_instance=RequestContext(request))
	#page = page[0]
	#return render_to_response(
		#'pages/add_comment.html',
		#{'page': page},
		#context_instance=RequestContext(request, {'current_book': page['current_book']}))
	

def search_pages(request):
	"""
	Search view using Google ajax search
	"""
	if request.POST:
		data = request.POST.copy()
		return render_to_response(
			'pages/search.html',
			{'term': data['term'], 'key': settings.GOOGLE_AJAX_SEARCH_API_KEY},
			context_instance=RequestContext(request)
			)
	else:
		return render_to_response('pages/search.html', {'key': key}, context_instance=RequestContext(request))
