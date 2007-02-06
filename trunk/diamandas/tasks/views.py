# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from tasks.models import *
from django.http import HttpResponseRedirect
from django.conf import settings
from stripogram import html2safehtml
from django import forms
from django.db.models import Q

# list tasks
def task_list(request, pagination_id):
	from django.views.generic.list_detail import object_list
	tasks = Task.objects.all().values('id', 'task_status', 'task_name', 'task_modification_date', 'is_sticky').order_by('-is_sticky', '-task_modification_date')
	if len(tasks) == 0:
		return render_to_response('tasks/task_list.html', {'sid': settings.SITE_ID})
	return object_list(request, tasks, paginate_by = 30, page = pagination_id, template_name = 'tasks/task_list.html', extra_context={'sid': settings.SITE_ID})

# show tasks
def task_show(request, task_id):
	task = Task.objects.get(id=task_id)
	users = task.task_assignedto.all()
	if len(users) > 0:
		user_list = ''
		for i in users:
			user_list = user_list + '<a href="/user/show_profile/' + str(i) + '/">' + str(i) + '</a> '
	else:
		user_list = _('None')
	com = TaskComment.objects.filter(com_task_id = task_id)
	return render_to_response('tasks/task_show.html', {'task': task, 'com': com, 'user_list': user_list, 'sid': settings.SITE_ID})

def com_task_add(request, task_id):
	if request.user.is_authenticated():
		if request.POST and len(request.POST['text']) > 0:
			task = Task.objects.get(id=task_id)
			text = html2safehtml(request.POST['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'pre', 'div', 'span', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'blockquote'))
			co = TaskComment(com_task_id = task, com_text = text, com_author = str(request.user), com_ip = request.META['REMOTE_ADDR'])
			co.save()
			task.save()
			from django.contrib.sites.models import Site
			from django.core.mail import mail_admins
			s = Site.objects.get(id=settings.SITE_ID)
			mail_admins('Komentarz Dodany', "Dodano komentarz: http://www." + str(s) + "/tasks/task_show/" + str(task_id) + '/', fail_silently=True)
			return HttpResponseRedirect('/tasks/task_show/' + str(task_id) + '/')
		else:
			return render_to_response('tasks/com_task_add.html', {'sid': settings.SITE_ID})
	return render_to_response('tasks/noperm.html', {'sid': settings.SITE_ID, 'why': _('You don\'t have the permissions to add coments. Are you logged in?')}) # can't view page
