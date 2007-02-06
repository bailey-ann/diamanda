from wiki.models import Page
from datetime import datetime
today = str(datetime.today())
day = int(today[6:7])
def render(dic, text):
	for i in dic:
		page = Page.objects.get(slug=i['attributes']['slug'])
		pday = str(page.date)
		pdday = int(pday[9:10])
		if today[:7] == pday[:7] and pdday >= day-3:
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/1.png" alt="" /> <a href="/w/p/' + page.slug + '/">' + page.title + '</a> - ' + page.description + ' <img src="/site_media/wiki/img/new_1.gif" alt="" /><br />')
		if today[:7] == pday[:7] and pdday >= day-10:
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/1.png" alt="" /> <a href="/w/p/' + page.slug + '/">' + page.title + '</a> - ' + page.description + ' <img src="/site_media/wiki/img/new_3.gif" alt="" /><br />')
		elif today[:7] == pday[:7]:
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/1.png" alt="" /> <a href="/w/p/' + page.slug + '/">' + page.title + '</a> - ' + page.description + ' <img src="/site_media/wiki/img/new_7.gif" alt="" / alt="" /><br />')
		else:
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/1.png" alt="" /> <a href="/w/p/' + page.slug + '/">' + page.title + '</a> - ' + page.description + '<br />')
	return text

def describe():
	return {'tag':'art', 'tag_example':_('[rk:art slug="SLUG_NAME"]'), 'description':_('Will insert a link to a given page (by the given slug) using it title and description')}
