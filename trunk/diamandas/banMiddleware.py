from django.shortcuts import render_to_response
bans = 'some ip'

class banMiddleware(object):
	def process_request(self, request):
		if bans.find(request.META['REMOTE_ADDR']) != -1:
			return render_to_response('ban.html') # baned


