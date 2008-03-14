
def forum(request):
	perms = {}
	if request.user.is_authenticated():
		perms['add_topic'] = True
		perms['add_post'] = True
		perms['is_authenticated'] = True
		perms['is_staff'] = request.user.is_staff
	else:
		perms['add_topic'] = False
		perms['add_post'] = False
		perms['is_staff'] = False
		
	return {'perms': perms, 'on_forum': True}