from django.shortcuts import render_to_response
from tasks.models import *
from wiki.models import Archive
from django.http import HttpResponseRedirect
from django.conf import settings
from stripogram import html2safehtml
from django import forms

# list tasks
def task_list(request, pagination_id):
	from django.views.generic.list_detail import object_list
	tasks = Task.objects.values('id', 'task_status', 'task_name', 'task_modification_date', 'task_progress', 'task_priority').order_by('-task_modification_date')
	proposals = Archive.objects.values('slug', 'title', 'modification_user', 'modification_date', 'changes').order_by('-modification_date').filter(is_proposal__exact=True)
	if request.user.is_authenticated() and request.user.has_perm('tasks.add_task'):
		add_task = True
	else:
		add_task = False
	if len(tasks) == 0:
		return render_to_response('tasks/' + settings.ENGINE + '/task_list.html', {'proposals': proposals, 'theme': settings.THEME, 'engine': settings.ENGINE})
	return object_list(request, tasks, paginate_by = 30, page = pagination_id, extra_context = {'theme': settings.THEME, 'engine': settings.ENGINE, 'proposals': proposals, 'add_task': add_task, 'perms': { 'add': request.user.has_perm('tasks.add_task'), 'change': request.user.has_perm('tasks.change_task'), 'delete' : request.user.has_perm('tasks.delete_task') } }, template_name = 'tasks/' + settings.ENGINE + '/task_list.html')

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
	if request.user.is_authenticated() and request.user.has_perm('tasks.add_task'):
		add_task = True
	else:
		add_task = False
	return render_to_response('tasks/' + settings.ENGINE + '/task_show.html', {'task': task, 'com': com, 'user_list': user_list, 'add_task': add_task, 'theme': settings.THEME, 'engine': settings.ENGINE ,'perms': {'add': request.user.has_perm('tasks.add_task'), 'change': request.user.has_perm('tasks.change_task'), 'delete' : request.user.has_perm('tasks.delete_task') }})

# add task
def task_add(request):
	if request.user.is_authenticated() and request.user.has_perm('tasks.add_task'):
		manipulator = Task.AddManipulator()
		if request.POST:
			data = request.POST.copy()
			data['task_status'] = _('Unassigned')
			data['task_priority'] = 'Minor'
			data['task_progress'] = '0'
			errors = manipulator.get_validation_errors(data)
			if not errors:
				manipulator.do_html2python(data)
				data['task_name'] = html2safehtml(data['task_name'] ,valid_tags=())
				data['task_text'] = html2safehtml(data['task_text'] ,valid_tags=('br', 'b', 'u', 'i', 'a'))
				data['task_type'] = html2safehtml(data['task_type'] ,valid_tags=())
				manipulator.save(data)
				return HttpResponseRedirect('/tasks/task_list/1')
		else:
			errors = {}
		data = {}
		form = forms.FormWrapper(manipulator, data, errors)
		return render_to_response('tasks/' + settings.ENGINE + '/task_add.html', {'form': form, 'theme': settings.THEME, 'engine': settings.ENGINE})
	return render_to_response('tasks/' + settings.ENGINE + '/noperm.html', {'theme': settings.THEME, 'engine': settings.ENGINE}) # can't view page

def com_task_add(request, task_id):
	if request.user.is_authenticated() and request.user.has_perm('tasks.add_taskcomment'):
		if request.POST and len(request.POST['text']) > 0:
			task = Task.objects.get(id=task_id)
			text = html2safehtml(request.POST['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'pre', 'div', 'span', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'blockquote'))
			co = TaskComment(com_task_id = task, com_text = text, com_author = str(request.user), com_ip = request.META['REMOTE_ADDR'])
			co.save()
			task.save()
			return HttpResponseRedirect('/tasks/task_show/' + str(task_id) + '/')
		else:
			return render_to_response('tasks/' + settings.ENGINE + '/com_task_add.html', {'theme': settings.THEME, 'engine': settings.ENGINE})
	return render_to_response('tasks/' + settings.ENGINE + '/noperm.html', {'theme': settings.THEME, 'engine': settings.ENGINE}) # can't view page
