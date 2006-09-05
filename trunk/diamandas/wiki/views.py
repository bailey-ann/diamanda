from django.shortcuts import render_to_response
from wiki.models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django import forms
from django.conf import settings
from django.contrib.auth.models import User, Group
from stripogram import html2safehtml

def users(request):
	from django.contrib.auth import authenticate, login
	if not request.user.is_authenticated():
		# captcha image creation
		from random import choice
		import Image, ImageDraw, ImageFont, sha
		# create a 5 char random strin and sha hash it
		imgtext = choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')
		imghash = sha.new(imgtext).hexdigest()
		# create an image with the string
		im=Image.open('/home/piotr/diamanda/media/bg.jpg')
		draw=ImageDraw.Draw(im)
		font=ImageFont.truetype("/home/piotr/diamanda/media/SHERWOOD.TTF", 18)
		draw.text((10,10),imgtext, font=font, fill=(100,100,50))
		im.save('/home/piotr/diamanda/media/bg2.jpg',"JPEG")
		
		# log in user
		if request.POST:
			data = request.POST.copy()
			# does the captcha math
			if data['imghash'] == sha.new(data['imgtext']).hexdigest():
				user = authenticate(username=data['login'], password=data['password'])
				if user is not None:
					login(request, user)
					return HttpResponseRedirect('/wiki/user/')
				else:
					return render_to_response('wiki/users.html', {'loginform': True, 'error': True, 'hash': imghash})
			else:
					return render_to_response('wiki/users.html', {'loginform': True, 'error': True, 'hash': imghash})
		# no post data, show the login forum
		else:
			return render_to_response('wiki/users.html', {'loginform': True, 'hash': imghash})
	else:
		# user authenticated, show his page with permissions
		if request.GET:
			# if /wiki/user/?log=out -> logout user
			data = request.GET.copy()
			if data['log'] == 'out':
				from django.contrib.auth import logout
				logout(request)
				return HttpResponseRedirect('/wiki/user/')
		# show the page
		return render_to_response('wiki/users.html', {'user': str(request.user), 'current': request.user.has_perm('wiki.can_set_current'), 'add': request.user.has_perm('wiki.add_page'), 'edit': request.user.has_perm('wiki.change_page')})

# register user
def register(request):
	from django.contrib.auth import authenticate, login
	# captcha image creation
	from random import choice
	import Image, ImageDraw, ImageFont, sha
	# create a 5 char random strin and sha hash it
	imgtext = choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')+choice('QWERTYUOPASDFGHJKLZXCVBNM')
	imghash = sha.new(imgtext).hexdigest()
	# create an image with the string
	im=Image.open('/home/piotr/diamanda/media/bg.jpg')
	draw=ImageDraw.Draw(im)
	font=ImageFont.truetype("/home/piotr/diamanda/media/SHERWOOD.TTF", 18)
	draw.text((10,10),imgtext, font=font, fill=(100,100,50))
	im.save('/home/piotr/diamanda/media/bg2.jpg',"JPEG")

	if request.POST:
		data = request.POST.copy()
		if data['password1'] == data['password2'] and len(data['password1']) > 4 and len(data['login']) > 3 and len(data['email']) >3 and data['password1'].isalnum() and data['login'].isalnum() and data['email'].find('@') != -1 and data['imghash'] == sha.new(data['imgtext']).hexdigest():
			data['email'] = html2safehtml(data['email'] ,valid_tags=())
			try:
				user = User.objects.create_user(data['login'], data['email'], data['password1'])
			except Exception:
				return render_to_response('wiki/register.html', {'error': True})
			else:
				user.save()
				user = authenticate(username=data['login'], password=data['password1'])
				if user is not None:
					login(request, user)
					user.groups.add(Group.objects.get(name='users'))
				return HttpResponseRedirect('/wiki/user/')
		else:
			return render_to_response('wiki/register.html', {'error': True, 'hash': imghash})
	else:
		return render_to_response('wiki/register.html', {'hash': imghash})

# Search using LIKE
def search_pages(request):
	if request.POST:
		data = request.POST.copy()
		if len(data['string']) > 3:
			pages = Page.objects.filter(text__icontains=data['string']).values('slug', 'title', 'description')
			return render_to_response('wiki/search.html', {'pages': pages, 'string': data['string']})
		else:
			return render_to_response('wiki/search.html')
	else:
		return render_to_response('wiki/search.html')

# List of categories and wiki pages
def index(request):
	categories = WikiCategory.objects.all()
	tree = ''
	for cat in categories:
		tree = tree +'<div style="padding-left:'+ str(int(cat.cat_depth)*20) +'px;"><img src="/site_media/wiki/img/category.png"> <b>' + str(cat) + '</b>'
		if cat.cat_description:
			tree = tree + ' - ' + str(cat.cat_description)
		pages = cat.page_set.all()
		if len(pages) > 0:
			tree = tree +'<div style="padding-left:5px; padding-bottom:3px;">'
			for page in pages:
				tree = tree + '<img src="/site_media/wiki/img/2.png"> <a href="/wiki/page/'+str(page.slug)+'/">' + str(page.title) + '</a> - ' + str(page.description) + '<br>'
			tree = tree + '</div>'
		tree = tree + '</div>';
	return render_to_response('wiki/main.html', {'tree': tree})

# show all edit proposals
def proposal_list(request):
	proposals = Archive.objects.order_by('-modification_date').filter(is_proposal__exact=True)
	return render_to_response('wiki/proposals.html', {'proposals': proposals})

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
			return render_to_response('wiki/noperm.html') # can't unpropose
	else:
		return render_to_response('wiki/noperm.html') # can't unpropose

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
			return render_to_response('wiki/indexPage.html', {'page': page, 'is_authenticated': request.user.is_authenticated(), 'pdf': pdf})
		else:
			return render_to_response('wiki/page.html', {'page': page, 'pdf': pdf})
	else:
		return render_to_response('wiki/noperm.html') # can't view page


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
		return render_to_response('wiki/noperm.html') # can't view page

# show achived page by given ID
def show_old_page(request, archive_id):
	# can user see the page (can_view) or anonymous "anonymous_can_view" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_view') or settings.ANONYMOUS_CAN_VIEW and not request.user.is_authenticated():
		try:
			page = Archive.objects.get(id__exact=archive_id)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/') # show some error message
		return render_to_response('wiki/oldPage.html', {'page': page})
	else:
		return render_to_response('wiki/noperm.html') # can't view page

# show list of changes for a page by given slug
def show_page_history_list(request, slug):
	# can user see the page (can_view) or anonymous "anonymous_can_view" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_view') or settings.ANONYMOUS_CAN_VIEW and not request.user.is_authenticated():
		try:
			page = Page.objects.get(slug__exact=slug)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/wiki/add/'+slug+'/')
		
		archive = Archive.objects.order_by('-modification_date').filter(page_id__exact=page.id)
		if request.user.is_authenticated():
			user_data = User.objects.get(username=str(request.user))
			is_staff = user_data.is_staff
		else:
			is_staff = False
		
		return render_to_response('wiki/page_history_list.html', {'page': page, 'archive': archive, 'is_staff': is_staff})
	else:
		return render_to_response('wiki/noperm.html') # can't view page

# restores an old version of a page by archive ID entry
def restore_page_from_archive(request, archive_id):
	if settings.USE_BANS:
		bans = Ban.objects.all()
		for ban in bans:
			if ban.ban_type == 'ip' and request.META['REMOTE_ADDR'].find(ban.ban_item) != -1:
				return render_to_response('wiki/ban.html')
			if ban.ban_type == 'dns' and request.META['REMOTE_HOST'].find(ban.ban_item) != -1:
				return render_to_response('wiki/ban.html')
	# can user set a page as current - can_set_current or anonymous "anonymous_can_set_current" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.can_set_current') or settings.ANONYMOUS_CAN_SET_CURENT and not request.user.is_authenticated():
		try:
			page_old = Archive.objects.get(id__exact=archive_id)
			pid = str(page_old.page_id)
			page_new = Page.objects.get(id__exact=pid)
		except Page.DoesNotExist:
			return HttpResponseRedirect('/') # no page, display error msg!
		# save old version as new, move current version to the archive
		old = Archive(page_id = page_new, title=page_new.title, slug = page_new.slug, description = page_new.description, text=page_new.text, changes = 'Moved to Archive. ('+ page_new.changes +')', modification_date = page_new.modification_date, modification_user = page_new.modification_user, modification_ip = page_new.modification_ip, modification_host = page_new.modification_host)
		old.save()
		page_new.title = page_old.title
		page_new.description = page_old.description
		page_new.text=page_old.text
		page_new.changes = _('Restored version ')+ str(page_old.id) +_(' from Archive. (') + page_old.changes + ')'
		page_new.modification_date = page_old.modification_date
		page_new.modification_user = str(request.user)
		page_new.modification_ip = request.META['REMOTE_ADDR']
		page_new.modification_host = request.META['REMOTE_HOST']
		page_new.save()
		return HttpResponseRedirect('/wiki/history/'+page_new.slug +'/')
	else:
		return render_to_response('wiki/noperm.html') # can't view page
	

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
			from difflib import unified_diff
			raw_result = list(unified_diff(page_old.text.split("\n"), page_new.text.split("\n")))
			html_result = ['<table class="diff" cellspacing="0" cellpadding="0">']
			for i in raw_result:
				if len(i) > 1 and i[0] == '+'  and i[1] != '+':
					html_result.append('<tr><td>+</td><td class="diffadd">' + i[1:] + '</td></tr>')
				elif len(i) > 1 and i[0] == '-' and i[1] != '-':
					html_result.append('<tr><td>-</td><td class="diffdel">' + i[1:] + '</td></tr>')
				elif len(i) > 0 and i[0] == '?':
					html_result.append('<tr><td>?</td><td class="diffchange">' + i[1:] + '</td></tr>')
				elif len(i) > 1 and i[0:2] == '@@':
					i = i.replace('@@', '').strip().split(' ')
					i = str(i[0]).split(',')
					html_result.append('<tr><td></td><td class="diffno"><br></td></tr><tr><td></td><td class="diffinfo"><B>' + _('Row') + '</B>: ' + str(i[0])[1:] + '</td></tr>')
				elif len(i) > 1 and i[0:2] != '++' and i[0:2] != '--':
					html_result.append('<tr><td width="15"></td><td class="diffno">' + i + '</td></tr>')
			html_result.append('</table>')
			return render_to_response('wiki/diff.html', {'diffresult': html_result, 'slug': page_new.slug})
		else:
			return render_to_response('wiki/noperm.html') # can't view page
	else:
		return HttpResponseRedirect('/') # no POST

# add a page
def add_page(request, slug=''):
	if settings.USE_BANS:
		bans = Ban.objects.all()
		for ban in bans:
			if ban.ban_type == 'ip' and request.META['REMOTE_ADDR'].find(ban.ban_item) != -1:
				return render_to_response('wiki/ban.html')
			if ban.ban_type == 'dns' and request.META['REMOTE_HOST'].find(ban.ban_item) != -1:
				return render_to_response('wiki/ban.html')
	# can user add the page (add_page) or anonymous "anonymous_can_add" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.add_page') or settings.ANONYMOUS_CAN_ADD and not request.user.is_authenticated():
		# check if the page exist
		try:
			page = Page.objects.get(slug__exact=slug)
		# page doesn't exist so we can add it
		except Page.DoesNotExist:
			manipulator = Page.AddManipulator()
			
			if request.POST:
				page_data = request.POST.copy()
				page_data['modification_user'] = str(request.user)
				page_data['modification_ip'] = request.META['REMOTE_ADDR']
				page_data['modification_host'] = request.META['REMOTE_HOST']
				errors = manipulator.get_validation_errors(page_data)
				if not errors:
					import re
					import base64
					tags = re.findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], re.MULTILINE)
					for i in tags:
						page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.b64encode(i[1])+'[/rk:syntax]')
					page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
					
					manipulator.do_html2python(page_data)
					new_place = manipulator.save(page_data)
					return HttpResponseRedirect("/wiki/page/" + page_data['slug'] +"/")
			else:
				errors = {}
				page_data = {'slug': slug}
			form = forms.FormWrapper(manipulator, page_data, errors)
			cbcdesc = Cbc.objects.all().order_by('tag')
			return render_to_response('wiki/add.html', {'form': form, 'cbcdesc': cbcdesc})
		# page exist
		else:
			return HttpResponseRedirect("/wiki/page/" + slug +"/")
	else:
		return render_to_response('wiki/noperm.html') # can't view page

# edit page by given slug
def edit_page(request, slug):
	if settings.USE_BANS:
		bans = Ban.objects.all()
		for ban in bans:
			if ban.ban_type == 'ip' and request.META['REMOTE_ADDR'].find(ban.ban_item) != -1:
				return render_to_response('wiki/ban.html')
			if ban.ban_type == 'dns' and request.META['REMOTE_HOST'].find(ban.ban_item) != -1:
				return render_to_response('wiki/ban.html')
	# can user change the page (change_page) or anonymous "anonymous_can_edit" in the settings.py
	if request.user.is_authenticated() and request.user.has_perm('wiki.change_page') or settings.ANONYMOUS_CAN_EDIT and not request.user.is_authenticated():
		import re
		import base64
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
			page_data['modification_host'] = request.META['REMOTE_HOST']
			errors = manipulator.get_validation_errors(page_data)
			if not errors:
				# encode rk:syntax code so we can stripp HTML etc. 
				tags = re.findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], re.MULTILINE)
				for i in tags:
					page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.b64encode(i[1])+'[/rk:syntax]')
				# change HTML to plain/text - markdown
				page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'table', 'tr', 'td', 'tbody', 'pre', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'img', 'thead', 'th', 'li', 'ul', 'ol', 'label', 'acronym', 'abbr', 'center', 'cite', 'map', 'strong', 'sub', 'sup', 'tfoot', 'blockquote'))
				# can user / anonymous set new changeset as current? wiki.can_set_current and settings.ANONYMOUS_CAN_SET_CURENT for anonymous
				if request.user.is_authenticated() and request.user.has_perm('wiki.can_set_current') or settings.ANONYMOUS_CAN_SET_CURENT and not request.user.is_authenticated():
					#save old version to Archive
					old = Archive(page_id = page, title=page.title, slug = page.slug, description = page.description, text=page.text, changes = page.changes, modification_date = page.modification_date, modification_user = page.modification_user, modification_ip = page.modification_ip, modification_host = page.modification_host)
					old.save()
					#set edit as current content
					manipulator.do_html2python(page_data)
					new_place = manipulator.save(page_data)
				else:
					# can't save as current - save as a "old" revision with...
					from datetime import datetime
					old = Archive(page_id = page, title=page_data['title'], slug = page_data['slug'], description = page_data['description'], text=page_data['text'], changes = page_data['changes'], modification_date = datetime.today(), modification_user = page_data['modification_user'], modification_ip = page_data['modification_ip'], modification_host = page_data['modification_host'], is_proposal=True)
					old.save()
				return HttpResponseRedirect("/wiki/page/" + page_data['slug'] +"/")
		else:
			errors = {}
		#page_data = page.__dict__
		page_data['changes'] = ''
		# decode rk:syntax code
		tags = re.findall( r'(?xs)\[\s*rk:syntax\s*(.*?)\](.*?)\[(?=\s*/rk)\s*/rk:syntax\]''', page_data['text'], re.MULTILINE)
		for i in tags:
			page_data['text'] = page_data['text'].replace('[rk:syntax '+i[0]+']'+i[1]+'[/rk:syntax]', '[rk:syntax '+i[0]+']'+base64.b64decode(i[1])+'[/rk:syntax]')
		form = forms.FormWrapper(manipulator, page_data, errors)
		cbcdesc = Cbc.objects.all().order_by('tag')
		return render_to_response('wiki/edit.html', {'form': form, 'page': page, 'cbcdesc': cbcdesc})
	else:
		return render_to_response('wiki/noperm.html') # can't view page

# List news
def list_news(request, pagination_id):
	from django.views.generic.list_detail import object_list
	return object_list(request, News.objects.all().order_by('-news_date'), paginate_by = 5, page = pagination_id)

# List news from category
def list_news_from_category(request, category_id, pagination_id):
	from django.views.generic.list_detail import object_list
	category = WikiCategory.objects.get(id=category_id)
	return object_list(request, category.news_set.all().order_by('-news_date'), template_name = 'wiki/news_list_category.html', paginate_by = 5, page = pagination_id, extra_context = {'category_id':category_id, 'category': category.cat_name})
