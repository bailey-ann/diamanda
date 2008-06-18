#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
from datetime import datetime, timedelta

from django.conf import settings

from myghtyboard.models import Forum, Post

def forum(request):
	perms = {}
	perms['add_topic'] = False
	perms['add_post'] = False
	perms['is_staff'] = False
	perms['is_authenticated'] = False
	perms['is_spam'] = False
	
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
		# check if forum allows posting for anonymous
		try:
			forum = Forum.objects.get(id=request.forum_id)
		except:
			pass
		else:
			if forum.allow_anonymous:
				check_date = datetime.now() - timedelta(hours=1)
				spam = Post.objects.filter(author_anonymous=True, date__gt=check_date).count()
				if spam < settings.FORUM_MAX_ANONYMOUS_PER_HOUR:
					perms['add_topic'] = True
					perms['add_post'] = True
				else:
					perms['is_spam'] = True
	return {'perms': perms, 'on_forum': True}