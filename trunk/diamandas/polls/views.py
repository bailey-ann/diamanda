#!/usr/bin/python
# Diamanda Application Set
# Polls

from stripogram import html2safehtml

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list

from polls.models import *

def show_polls(request):
	"""
	List all polls
	"""
	poll = Poll.objects.all().order_by('-id')
	return object_list(request, poll, paginate_by = 10, allow_empty = True, extra_context = {}, template_name = 'polls/poll_polls.html')

def show_pcomment(request, pid):
	"""
	Show a poll and poll comments
	
	* pid - ID of a Poll entry
	"""
	try:
		poll = Poll.objects.select_related().get(id=pid)
		com = PollComment.objects.filter(content=pid).order_by('-id')
	except:
		return render_to_response(
			'pages/bug.html',
			{'bug': _('Poll doesn\'t exist')},
			context_instance=RequestContext(request))
	
	# user can't add 3 comments in a row
	if com and com[0].author == request.user:
		add = False
	else:
		add = True

	# user can't vote more than once
	try:
		vcheck = Vote.objects.get(poll = poll, voter = request.user)
	except:
		vcheck = True
	else:
		vcheck = False
	
	total = 0
	choice = {}
	for votes in poll.choice_set.all():
		total = total + votes.votes
		choice[votes.id] = [votes.votes, votes.choice]
	
	if total > 0:
		choices = []
		for ch in choice:
			choices.append([(choice[ch][0]*100)/total, choice[ch][1]])
	else:
		choices = False

	if request.user.is_authenticated() and request.POST and request.POST.has_key('text') and len(request.POST['text']) > 2 and add:
		text = html2safehtml(request.POST['text'] ,valid_tags=('b', 'u', 'i', 'br', 'blockquote'))
		text = text.replace("\n", "<br />")
		co = PollComment(content = poll, text = text, author = request.user)
		co.save()
		return HttpResponseRedirect('/p/' + str(pid) + '/')
	if request.user.is_authenticated() and request.POST and request.POST.has_key('vote') and vcheck:
		try:
			c = Choice.objects.get(id = request.POST['vote'])
		except:
			pass
		else:
			v = Vote(poll = poll, voter = request.user)
			v.save()
			c = Choice.objects.get(id = request.POST['vote'])
			c.votes = c.votes + 1
			c.save()
		return HttpResponseRedirect('/p/' + str(pid) + '/')
	return render_to_response(
		'polls/poll_show.html',
		{'page': com, 'p': poll, 'add':add, 'vcheck':vcheck, 'choices':choices},
		context_instance=RequestContext(request))