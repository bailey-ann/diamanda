#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from myghtyboard.models import Forum

def forum(request):
	perms = {}
	perms['add_topic'] = False
	perms['add_post'] = False
	perms['is_staff'] = False
	perms['is_authenticated'] = False
	
	if request.user.is_authenticated():
		perms['add_topic'] = True
		perms['add_post'] = True
		perms['is_authenticated'] = True
		perms['is_staff'] = request.user.is_staff
		
		if hasattr(request, 'forum_id'):
			try:
				forum = Forum.objects.get(id=request.forum_id)
			except:
				pass
			else:
				if forum.use_moderators and request.user in forum.moderators.all():
					perms['add_topic'] = True
					perms['add_post'] = True
					perms['is_authenticated'] = True
					perms['is_staff'] = True
	elif not request.user.is_authenticated() and hasattr(request, 'forum_id'):
		try:
			forum = Forum.objects.get(id=request.forum_id)
		except:
			pass
		else:
			if forum.allow_anonymous:
				perms['add_topic'] = True
				perms['add_post'] = True
	return {'perms': perms, 'on_forum': True}