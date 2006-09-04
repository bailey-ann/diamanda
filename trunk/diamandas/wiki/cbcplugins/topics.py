from myghtyboard.models import *
def render(dic, text):
	for i in dic:
		if i['attributes']['forum'] == '0':
			topics = Topic.objects.all().order_by('-topic_modification_date')[:10]
		else:
			forum = i['attributes']['forum']
			topics = Topic.objects.order_by('-topic_modification_date').filter(topic_forum=forum)[:10]
		tree = ''
		for t in topics:
			lastposter = str(t.topic_lastpost)
			br = lastposter.find('<br>')
			tree = tree + '<img src="/site_media/wiki/img/2.png"> <a href="/forum/topic/1/' + str(t.id) + '/">' + str(t.topic_name) + '</a> (' + lastposter[:br] + ')<br>'
		text = text.replace(i['tag'], tree)
		del topics
	return text
