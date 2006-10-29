from django.shortcuts import render_to_response
from wiki.models import *
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from stripogram import html2safehtml
from wiki.cbcparser import *
from django.core import validators

# Search using LIKE and or google
def search_pages(request):
	if settings.WIKI_GOOGLE_SEARCH_API:
		google = True
	else:
		google = False
	if request.POST:
		data = request.POST.copy()
		if len(data['string']) > 3:
			if data.has_key('like'):
				pages = Page.objects.filter(text__icontains=data['string']).values('slug', 'title', 'description')
				return render_to_response('wiki/search.html', {'pages': pages, 'string': data['string'], 'google': google, 'css_theme': settings.CSS_THEME})
			else:
				try:
					import google
					google.setLicense(settings.WIKI_GOOGLE_SEARCH_API)
					pages = google.doGoogleSearch(data['string'] + ' site:' + str(Site.objects.get_current()))
					pages = pages.results
				except Exception:
					return render_to_response('wiki/search.html', {'pages': False, 'string': data['string'], 'google': google, 'css_theme': settings.CSS_THEME})
				else:
					return render_to_response('wiki/search.html', {'pages': pages, 'string': data['string'], 'google': google, 'googleuse': True, 'css_theme': settings.CSS_THEME})
		else:
			return render_to_response('wiki/search.html', {'google': google, 'css_theme': settings.CSS_THEME})
	else:
		return render_to_response('wiki/search.html', {'google': google, 'css_theme': settings.CSS_THEME})

def index(request):
	pages = Page.objects.all()
	tree = ''
	for page in pages:
		tree = tree + '<img src="/site_media/wiki/img/2.png" alt="" /> <a href="/wiki/page/'+str(page.slug)+'/">' + str(page.title) + '</a> - ' + str(page.description) + '<br />'
	return render_to_response('wiki/main.html', {'tree': tree, 'css_theme': settings.CSS_THEME})

# sets proposal as a normal archive entry
def unpropose(request, archive_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			try:
				archive_entry = Archive.objects.get(id = archive_id)
			except Page.DoesNotExist:
				return HttpResponseRedirect('/')
			else:
				archive_entry.is_proposal = False
				archive_entry.save()
				return HttpResponseRedirect('/wiki/history/' + archive_entry.slug + '/')
		else:
			return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't unpropose
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't unpropose

# show the page by given slug
def show_page(request, slug='index'):	
	# can user see the page (can_view) or anonymous "anonymous_can_view" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_view') or settings.ANONYMOUS_CAN_VIEW and not request.user.is_authenticated():
		try:
			page = Page.objects.get(slug__exact=slug)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/wiki/add/'+slug+'/')
		if settings.WIKI_USE_PDF:
			pdf = True
		else:
			pdf = False
		if (slug == 'index'):
			return render_to_response('wiki/indexPage.html', {'page': page, 'is_authenticated': request.user.is_authenticated(), 'pdf': pdf, 'css_theme': settings.CSS_THEME})
		else:
			return render_to_response('wiki/page.html', {'page': page, 'pdf': pdf, 'css_theme': settings.CSS_THEME})
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page


# show the page by given slug - export it as PDF
# using htmldoc
def show_page_as_pdf(request, slug='index'):
	# can user see the page (can_view) or anonymous "anonymous_can_view" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_view') and settings.WIKI_USE_PDF == 'htmldoc' or settings.ANONYMOUS_CAN_VIEW and not request.user.is_authenticated() and settings.WIKI_USE_PDF == 'htmldoc':
		try:
			page = Page.objects.get(slug__exact=slug)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/wiki/add/'+slug+'/')
		import os
		from django.template import Context, loader
		t = loader.get_template('wiki/pdfpage.html')
		c = Context({
			'page': page,
		})
		
		(stin,stout) = os.popen2('htmldoc --webpage -t pdf --jpeg -')
		stin.write(t.render(c))
		stin.close()
		pdf = stout.read()
		stout.close()
		response = HttpResponse()
		response['Pragma'] = 'public'
		response['Content-Disposition'] = 'attachment; filename="' +str(page.title)+'"'
		response['Content-Type'] = 'application/pdf'
		response['Content-Transfer-Encoding'] = 'binary'
		response['Cache-Control'] = 'private'
		response['Content-Length'] = str(len(pdf))
		response.write(pdf)
		return response
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page

# show achived page by given ID
def show_old_page(request, archive_id):
	# can user see the page (can_view) or anonymous "anonymous_can_view" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_view') or settings.ANONYMOUS_CAN_VIEW and not request.user.is_authenticated():
		try:
			page = Archive.objects.get(id__exact=archive_id)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/') # show some error message
		return render_to_response('wiki/oldPage.html', {'page': page, 'css_theme': settings.CSS_THEME})
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page

# show list of changes for a page by given slug
def show_page_history_list(request, slug):
	# can user see the page (can_view) or anonymous "anonymous_can_view" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_view') or settings.ANONYMOUS_CAN_VIEW and not request.user.is_authenticated():
		try:
			page = Page.objects.get(slug__exact=slug)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/wiki/add/'+slug+'/')
		page.modification_date = str(page.modification_date)[:16]
		archive = Archive.objects.order_by('-modification_date').filter(page_id__exact=page.id)
		if request.user.is_authenticated():
			user_data = User.objects.get(username=str(request.user))
			is_staff = user_data.is_staff
		else:
			is_staff = False
		if len(archive) > 0:
			for i in archive:
				i.modification_date = str(i.modification_date)[:16]
		return render_to_response('wiki/page_history_list.html', {'page': page, 'archive': archive, 'is_staff': is_staff, 'css_theme': settings.CSS_THEME})
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page

# restores an old version of a page by archive ID entry
def restore_page_from_archive(request, archive_id):
	if settings.USE_BANS:
		bans = Ban.objects.all()
		for ban in bans:
			if request.META['REMOTE_ADDR'].find(ban.ban_item) != -1:
				return render_to_response('wiki/ban.html', {'css_theme': settings.CSS_THEME})
	# can user set a page as current - can_set_current or anonymous "anonymous_can_set_current" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_set_current') or settings.ANONYMOUS_CAN_SET_CURENT and not request.user.is_authenticated():
		try:
			page_old = Archive.objects.get(id__exact=archive_id)
			pid = str(page_old.page_id)
			page_new = Page.objects.get(id__exact=pid)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/') # no page, display error msg!
		# save old version as new, move current version to the archive
		old = Archive(page_id = page_new, title=page_new.title, slug = page_new.slug, description = page_new.description, text=page_new.text, changes = 'Moved to Archive. ('+ page_new.changes +')', modification_date = page_new.modification_date, modification_user = page_new.modification_user, modification_ip = page_new.modification_ip)
		old.save()
		page_new.title = page_old.title
		page_new.description = page_old.description
		page_new.text=page_old.text
		page_new.changes = _('Restored version ')+ str(page_old.id) +_(' from Archive. (') + page_old.changes + ')'
		page_new.modification_date = page_old.modification_date
		page_new.modification_user = str(request.user)
		page_new.modification_ip = request.META['REMOTE_ADDR']
		page_new.save()
		return HttpResponseRedirect('/wiki/history/'+page_new.slug +'/')
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page
	

# show diff between two entries. IF new = 0 then archive and current, if new !=0 - also archive
def show_diff(request):
	# can user see the page (can_view) or anonymous "anonymous_can_view" in the settings.py
	if request.POST and request.POST.has_key('old') and request.POST.has_key('new'):
		if request.user.is_authenticated() and request.user.has_perm('wiki.can_view') or settings.ANONYMOUS_CAN_VIEW and not request.user.is_authenticated():
			old = int(request.POST['old'])
			new = int(request.POST['new'])
			try:
				page_old = Archive.objects.get(id__exact=old)
				pid = str(page_old.page_id)
				if new == 0:
					page_new = Page.objects.get(id__exact=pid)
				else:
					page_new = Archive.objects.get(id__exact=new)
			except Page.DoesNotExist:
				return HttpResponseRedirect('/') # show some error message
			#from difflib import unified_diff
			#raw_result = list(unified_diff(page_old.text.split("\n"), page_new.text.split("\n")))
			import diff
			html_result = diff.textDiff(page_old.text, page_new.text)
			
			#html_result = []
			#for i in raw_result:
				#if len(i) > 1 and i[0] == '+'  and i[1] != '+':
					#html_result.append('<div class="diffadd">' + i[1:] + '</div>')
				#elif len(i) > 1 and i[0] == '-' and i[1] != '-':
					#html_result.append('<div class="diffdel">' + i[1:] + '</div>')
				#elif len(i) > 0 and i[0] == '?':
					#html_result.append('<div class="diffchange">' + i[1:] + '</div>')
				#elif len(i) > 1 and i[0:2] == '@@':
					#i = i.replace('@@', '').strip().split(' ')
					#i = str(i[0]).split(',')
					#html_result.append('<br /><div class="diffinfo"><b>' + _('Row') + '</b>: ' + str(i[0])[1:] + '</div>')
				#elif len(i) > 1 and i[0:2] != '++' and i[0:2] != '--':
					#html_result.append('<div class="diffno">' + i + '</div>')
			return render_to_response('wiki/diff.html', {'diffresult': html_result, 'slug': page_new.slug, 'css_theme': settings.CSS_THEME})
		else:
			return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page
	else:
		return HttpResponseRedirect('/') # no POST

# add a page
def add_page(request, slug=''):
	if settings.USE_BANS:
		bans = Ban.objects.all()
		if request.META['REMOTE_ADDR'].find(ban.ban_item) != -1:
			return render_to_response('wiki/ban.html', {'css_theme': settings.CSS_THEME})
	# can user add the page (add_page) or anonymous "anonymous_can_add" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.add_page') or settings.ANONYMOUS_CAN_ADD and not request.user.is_authenticated():
		# check if the page exist
		try:
			page = Page.objects.get(slug__exact=slug)
		# page doesn't exist so we can add it
		except Page.DoesNotExist:
			manipulator = Page.AddManipulator()
			from re import findall, MULTILINE
			import base64
			preview = False
			cbcerrors = False
			if request.POST:
				page_data = request.POST.copy()
				page_data['modification_user'] = str(request.user)
				page_data['modification_ip'] = request.META['REMOTE_ADDR']
				errors = manipulator.get_validation_errors(page_data)
				tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
				for i in tags:
					page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.encodestring(i[1])+'[/rk:syntax]')
				page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
				try:
					parse_cbc_tags(page_data['text'])
				except:
					cbcerrors = True
				
				if not errors and not page_data.has_key('preview') and not cbcerrors:
					manipulator.do_html2python(page_data)
					new_place = manipulator.save(page_data)
					return HttpResponseRedirect("/wiki/page/" + page_data['slug'] +"/")
				elif page_data.has_key('preview') and not cbcerrors:
					preview = page_data['text']
					tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', preview, MULTILINE)
					for i in tags:
						preview = preview.replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.encodestring(i[1])+'[/rk:syntax]')
					preview = html2safehtml(preview ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
			else:
				errors = {}
				page_data = {'slug': slug}
			form = forms.FormWrapper(manipulator, page_data, errors)
			cbcdesc = Cbc.objects.all().order_by('tag')
			return render_to_response('wiki/add.html', {'form': form, 'cbcdesc': cbcdesc, 'preview': preview, 'cbcerrors': cbcerrors, 'css_theme': settings.CSS_THEME})
		# page exist
		else:
			return HttpResponseRedirect("/wiki/page/" + slug +"/")
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page

# edit page by given slug
def edit_page(request, slug):
	if settings.USE_BANS:
		bans = Ban.objects.all()
		if request.META['REMOTE_ADDR'].find(ban.ban_item) != -1:
			return render_to_response('wiki/ban.html', {'css_theme': settings.CSS_THEME})
	# can user change the page (change_page) or anonymous "anonymous_can_edit" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.change_page') or settings.ANONYMOUS_CAN_EDIT and not request.user.is_authenticated():
		from re import findall, MULTILINE
		import base64
		preview = False
		cbcerrors = False
		try:
			page_id = Page.objects.get(slug__exact=slug)
			manipulator = Page.ChangeManipulator(page_id.id)
			page_data = manipulator.flatten_data()
		except Page.DoesNotExist:
			return HttpResponseRedirect('/wiki/add/'+slug+'/')
		page = manipulator.original_object
		if request.POST:
			page_data = request.POST.copy()
			page_data['slug'] = page.slug
			page_data['modification_user'] = str(request.user)
			page_data['modification_ip'] = request.META['REMOTE_ADDR']
			# encode rk:syntax code so we can stripp HTML etc. 
			tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.encodestring(i[1])+'[/rk:syntax]')
			page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
			import sys, traceback
			try:
				parse_cbc_tags(page_data['text'])
			except:
				afile = AFile()
				traceback.print_exc(file=afile)
				cbcerrors = afile.read()
				tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
				for i in tags:
					page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.decodestring(i[1])+'[/rk:syntax]')
			errors = manipulator.get_validation_errors(page_data)
			if not errors and not page_data.has_key('preview') and not cbcerrors:
				# can user / anonymous set new changeset as current? wiki.can_set_current and settings.ANONYMOUS_CAN_SET_CURENT for anonymous
				if request.user.is_authenticated() and request.user.has_perm('wiki.can_set_current') or settings.ANONYMOUS_CAN_SET_CURENT and not request.user.is_authenticated():
					#save old version to Archive
					old = Archive(page_id = page, title=page.title, slug = page.slug, description = page.description, text=page.text, changes = page.changes, modification_date = page.modification_date, modification_user = page.modification_user, modification_ip = page.modification_ip)
					old.save()
					#set edit as current content
					manipulator.do_html2python(page_data)
					new_place = manipulator.save(page_data)
				else:
					# can't save as current - save as a "old" revision with...
					from datetime import datetime
					old = Archive(page_id = page, title=page_data['title'], slug = page_data['slug'], description = page_data['description'], text=page_data['text'], changes = page_data['changes'], modification_date = datetime.today(), modification_user = page_data['modification_user'], modification_ip = page_data['modification_ip'], is_proposal=True)
					old.save()
				return HttpResponseRedirect("/wiki/page/" + page_data['slug'] +"/")
			elif page_data.has_key('preview') and not cbcerrors:
				preview = page_data['text']
				tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', preview, MULTILINE)
				for i in tags:
					preview = preview.replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.encodestring(i[1])+'[/rk:syntax]')
				preview = html2safehtml(preview ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
		else:
			errors = {}
			#page_data = page.__dict__
			page_data['changes'] = ''
			# decode rk:syntax code
			tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.decodestring(i[1])+'[/rk:syntax]')
		form = forms.FormWrapper(manipulator, page_data, errors)
		cbcdesc = Cbc.objects.all().order_by('tag')
		return render_to_response('wiki/edit.html', {'form': form, 'page': page, 'cbcdesc': cbcdesc, 'preview': preview, 'cbcerrors': cbcerrors, 'css_theme': settings.CSS_THEME})
	else:
		return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page


# list tasks
def task_list(request, pagination_id):
	from django.views.generic.list_detail import object_list
	tasks = Task.objects.values('id', 'task_status', 'task_name', 'task_modification_date', 'task_progress', 'task_priority').order_by('-task_modification_date')
	proposals = Archive.objects.values('slug', 'title', 'modification_user', 'modification_date', 'changes').order_by('-modification_date').filter(is_proposal__exact=True)
	if request.user.is_authenticated() and request.user.has_perm('wiki.add_task'):
		add_task = True
	else:
		add_task = False
	if len(tasks) == 0:
		return render_to_response('wiki/task_list.html', {'proposals': proposals, 'css_theme': settings.CSS_THEME})
	return object_list(request, tasks, paginate_by = 30, page = pagination_id, extra_context = {'proposals': proposals, 'add_task': add_task, 'perms': { 'add': request.user.has_perm('wiki.add_task'), 'change': request.user.has_perm('wiki.change_task'), 'delete' : request.user.has_perm('wiki.delete_task') } }, template_name = 'wiki/task_list.html')

# show tasks
def task_show(request, task_id):
	task = Task.objects.get(id=task_id)
	users = task.task_assignedto.all()
	if len(users) > 0:
		user_list = ''
		for i in users:
			user_list = user_list + str(i) + ' '
	else:
		user_list = _('None')
	com = TaskComment.objects.filter(com_task_id = task_id)
	if request.user.is_authenticated() and request.user.has_perm('wiki.add_task'):
		add_task = True
	else:
		add_task = False
	return render_to_response('wiki/task_show.html', {'task': task, 'com': com, 'user_list': user_list, 'add_task': add_task, 'css_theme': settings.CSS_THEME ,'perms': {'add': request.user.has_perm('wiki.add_task'), 'change': request.user.has_perm('wiki.change_task'), 'delete' : request.user.has_perm('wiki.delete_task') }})

def com_task_add(request, task_id):
	if request.user.is_authenticated() and request.user.has_perm('wiki.add_taskcomment'):
		if request.POST and len(request.POST['text']) > 0:
			task = Task.objects.get(id=task_id)
			text = html2safehtml(request.POST['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'pre', 'div', 'span', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'blockquote'))
			co = TaskComment(com_task_id = task, com_text = text, com_author = str(request.user), com_ip = request.META['REMOTE_ADDR'])
			co.save()
			task.save()
			return HttpResponseRedirect('/wiki/task_show/' + str(task_id) + '/')
		else:
			return render_to_response('wiki/com_task_add.html', {'css_theme': settings.CSS_THEME})
	return render_to_response('wiki/noperm.html', {'css_theme': settings.CSS_THEME}) # can't view page

# file like object (for storing cbc tracebacks)
class AFile(object):
	__content = '' 
	def write(self, txt): 
		self.__content += txt 
	def read(self): 
		return self.__content 