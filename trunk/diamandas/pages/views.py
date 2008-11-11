#!/usr/bin/python
# Diamanda Application Set
# Pages module

from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django import forms
from django.core.mail import mail_admins

from diamandas.pages.models import *
from diamandas.userpanel.models import Profile
from diamandas.myghtyboard.models import *
from diamandas.myghtyboard.context import forum as forumContext
from diamandas.myghtyboard import modelwrappers as diamandaModelwrappers
from diamandas.utils import *


def show_index(request):
	"""
	Show the main page
	"""
	try:
		feed = Feed.objects.get(site=settings.SITE_ID)
		feed = feed.html
	except:
		feed = False
	now = datetime.now()
	check_time = now - timedelta(minutes=10)
	onsite = Profile.objects.select_related().filter(onsitedata__gt=check_time).order_by('-onsitedata')[:4]
	try:
		p = Content.objects.get(slug='index')
	except:
		home = settings.DEFAULT_HOME_TEXT
		intro = settings.DEFAULT_HOME_INTRO
	else:
		home = p.text
		intro = p.description
	return render_to_response(
		'pages/show_index.html',
		{'onsite': onsite, 'home_text': home, 'feed': feed, 'intro': intro},
		context_instance=RequestContext(request))

def show_help(request):
	rss = Content.objects.filter(content_type='book').values('slug', 'title')
	return render_to_response(
		'pages/show_help.html',
		{'email': settings.SITE_ADMIN_MAIL, 'rss': rss},
		context_instance=RequestContext(request, {'on_help': True}))

def list_news(request, book=False):
	"""
	List news
	
	* book - slug of a Content entry (book content_type)
	"""
	if book:
		bk = Content.objects.get(slug=book)
		news = Content.objects.filter(content_type='news', place=bk).order_by('-date')
		count = news.count()
		count = count/10
		cnt = [1]
		i = 1
		while i <= count:
			i = i+1
			cnt.append(i)
		return object_list(
			request,
			news,
			paginate_by = 10,
			allow_empty = True,
			template_name = 'pages/news_list.html',
			extra_context = {'book': book, 'bk':bk, 'current_book': bk.slug, 'cnt': cnt})
	else:
		news = Content.objects.filter(content_type='news').order_by('-date')
	count = news.count()
	count = count/10
	cnt = [1]
	i = 1
	while i <= count:
		i = i+1
		cnt.append(i)
	return object_list(
		request,
		news,
		paginate_by = 10,
		allow_empty = True,
		template_name = 'pages/news_list.html',
		extra_context = {'book': book, 'cnt':cnt})

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
	
	if add_topic and not page.coment_topic:
		form = diamandaModelwrappers.AddTopicForm()
	elif add_topic and page.coment_topic:
		form = diamandaModelwrappers.AddPostForm()
	else:
		form = False
	
	comments = False
	# check if user wants to add a comment - show the form if possible
	if 'c' in request.GET:
		show_comment = True
		if form and page.coment_topic:
			comments = page.coment_topic.post_set.all().order_by('-id')[:10]
	else:
		show_comment = False
	
	if request.POST and add_topic and not page.coment_topic:
		COMMENT_POST = _('This is a discussion about article') + ': [url="/w/p/%s/"]%s[/url].' % (page.slug, page.title)
		REDIRECT = ("/w/p/" + slug +"/?c=ok", _('Comment added succesfuly.'))
		TITLE = _('Comments for: %s') % page.title
		return diamandaModelwrappers.add_topic(request, coment_forum_id, inject_post=COMMENT_POST, inject_title=TITLE, redirect_link=REDIRECT, content_obj=page)
	elif request.POST and add_topic and page.coment_topic:
		REDIRECT = ("/w/p/" + slug +"/?c=ok", _('Comment added succesfuly.'))
		return diamandaModelwrappers.add_post(request, page.coment_topic.id, redirect_link=REDIRECT, content_obj=page)
	
	if page.current_book:
		cb = page.current_book
	
	if page.content_type == 'news':
		return render_to_response(
			'pages/show_news.html',
			{'page': page, 'add_topic': add_topic, 'form': form, 'show_comment': show_comment, 'comments': comments},
			context_instance=RequestContext(request, {'current_book': cb}))
	return render_to_response(
		'pages/show.html',
		{'page': page, 'add_topic': add_topic, 'form': form, 'show_comment': show_comment, 'comments': comments},
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
	try:
		feed = Feed.objects.get(site=settings.SITE_ID)
		feed = feed.rss
	except:
		feed = False
	return HttpResponse(feed)

def book_rss(request, slug):
	"""
	RSS channel for a book
	
	* book - slug of a Content entry (book content_type)
	"""
	book = Content.objects.get(slug=slug)
	pages = Content.objects.filter(place=book).values('slug', 'title',
		'description', 'date', 'content_type').order_by('-id')[:10]
	return render_to_response('pages/rss1.html', {'pages': pages, 'book': book}, context_instance=RequestContext(request))

def content_rss(request):
	"""
	RSS channel for all pages
	"""
	pages = Content.objects.all().values('slug', 'title',
		'description', 'date', 'content_type').order_by('-id')[:10]
	return render_to_response('pages/rss.html', {'pages': pages}, context_instance=RequestContext(request))

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
		return render_to_response('pages/search.html', {'key': settings.GOOGLE_AJAX_SEARCH_API_KEY}, context_instance=RequestContext(request))
