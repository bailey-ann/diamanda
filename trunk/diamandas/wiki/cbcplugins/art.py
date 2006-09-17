from wiki.models import *
def render(dic, text):
	for i in dic:
		page = Page.objects.get(slug=i['attributes']['slug'])
		text = text.replace(i['tag'], '<img src="/site_media/wiki/img/1.png" alt="" /> <a href="/wiki/page/' + page.slug + '/">' + page.title + '</a> - ' + page.description + '<br />')
	return text
