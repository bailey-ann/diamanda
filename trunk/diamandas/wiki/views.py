from django.shortcuts import render_to_response
from wiki.models import *
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core import validators
from cbcplugins import cbcparser
from stripogram import html2safehtml
from django.http import HttpResponse

# sets proposal as a normal archive entry
def unpropose(request, archive_id):
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_set_current'):
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
			return render_to_response('wiki/noperm.html', {}) # can't unpropose
	else:
		return render_to_response('wiki/noperm.html', {}) # can't unpropose

# show the page by given slug
def show_page(request, slug='index'):
	try:
		page = Page.objects.get(slug__exact=slug)
	except Page.DoesNotExist:
		return HttpResponseRedirect('/wiki/add/'+slug+'/')
	if (slug == 'index'):
		return render_to_response('wiki/indexPage.html', {'page': page, 'is_authenticated': request.user.is_authenticated()})
	else:
		return render_to_response('wiki/page.html', {'page': page})

# show achived page by given ID
def show_old_page(request, archive_id):
	try:
		page = Archive.objects.get(id__exact=archive_id)
	except Page.DoesNotExist:
		return HttpResponseRedirect('/') # show some error message
	return render_to_response('wiki/oldPage.html', {'page': page})

# show list of changes for a page by given slug
def show_page_history_list(request, slug):
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
	return render_to_response('wiki/page_history_list.html', {'page': page, 'archive': archive, 'is_staff': is_staff, })
	
# restores an old version of a page by archive ID entry
def restore_page_from_archive(request, archive_id):
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
		return render_to_response('wiki/noperm.html', {}) # can't view page
	

# show diff between two entries. IF new = 0 then archive and current, if new !=0 - also archive
def show_diff(request):
	if request.POST and request.POST.has_key('old') and request.POST.has_key('new'):
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
			return HttpResponseRedirect('/')
		import diff
		html_result = diff.textDiff(page_old.text, page_new.text)
		return render_to_response('wiki/diff.html', {'diffresult': html_result, 'slug': page_new.slug, })
	else:
		return HttpResponseRedirect('/') # no POST

# add a page
def add_page(request, slug=''):
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
				
				page_data['title'] = html2safehtml(page_data['title'] ,valid_tags=())
				page_data['description'] = html2safehtml(page_data['description'] ,valid_tags=())
				page_data['changes'] = html2safehtml(page_data['changes'] ,valid_tags=())
				
				tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
				for i in tags:
					page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.encodestring(i[1])+'[/rk:syntax]')
				page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
				tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
				for i in tags:
					page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.decodestring(i[1])+'[/rk:syntax]')
				try:
					cbcparser.parse_cbc_tags(page_data['text'])
				except:
					cbcerrors = True
				# all ok, save it
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
					tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', preview, MULTILINE)
					for i in tags:
						preview = preview.replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.decodestring(i[1])+'[/rk:syntax]')
			else:
				errors = {}
				page_data = {'slug': slug}
			form = forms.FormWrapper(manipulator, page_data, errors)
			cbcdesc = cbcparser.list_descriptions()
			return render_to_response('wiki/add.html', {'form': form, 'cbcdesc': cbcdesc, 'preview': preview, 'cbcerrors': cbcerrors, })
		# page exist
		else:
			return HttpResponseRedirect("/wiki/page/" + slug +"/")
	else:
		return render_to_response('wiki/noperm.html', {}) # can't view page

# edit page by given slug
def edit_page(request, slug):
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
			page_data['title'] = html2safehtml(page_data['title'] ,valid_tags=())
			page_data['description'] = html2safehtml(page_data['description'] ,valid_tags=())
			page_data['changes'] = html2safehtml(page_data['changes'] ,valid_tags=())
			# encode rk:syntax code so we can stripp HTML etc.
			tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.encodestring(i[1])+'[/rk:syntax]')
			page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
			tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.decodestring(i[1])+'[/rk:syntax]')
			import sys, traceback
			try:
				cbcparser.parse_cbc_tags(page_data['text'])
			except:
				afile = AFile()
				traceback.print_exc(file=afile)
				cbcerrors = afile.read()
			errors = manipulator.get_validation_errors(page_data)
			if not errors and not page_data.has_key('preview') and not cbcerrors:
				# can user / anonymous set new changeset as current? wiki.can_set_current and settings.ANONYMOUS_CAN_SET_CURENT for anonymous
				if request.user.is_authenticated() and request.user.has_perm('wiki.can_set_current') or settings.ANONYMOUS_CAN_SET_CURENT and not request.user.is_authenticated():
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
				tags = findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', preview, MULTILINE)
				for i in tags:
					preview = preview.replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.decodestring(i[1])+'[/rk:syntax]')
		else:
			errors = {}
			#page_data = page.__dict__
			page_data['changes'] = ''
		form = forms.FormWrapper(manipulator, page_data, errors)
		cbcdesc = cbcdesc = cbcparser.list_descriptions()
		return render_to_response('wiki/edit.html', {'form': form, 'page': page, 'cbcdesc': cbcdesc, 'preview': preview, 'cbcerrors': cbcerrors, })
	else:
		return render_to_response('wiki/noperm.html', {}) # can't view page

# file like object (for storing cbc tracebacks)
class AFile(object):
	__content = ''
	def write(self, txt):
		self.__content += txt
	def read(self):
		return self.__content