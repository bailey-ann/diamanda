from wiki.models import *
def render(dic, text):
	for i in dic:
		category = WikiCategory.objects.get(cat_name=i['attributes']['name'])
		tree = ''
		news = category.news_set.all()[:5]
		if len(news) > 0:
			tree = tree +'<div style="padding-left:5px; padding-bottom:3px;">'
			for new in news:
				tree = tree + '<img src="/site_media/wiki/img/2.png"> <a href="/wiki/news/1/' + str(category.id) + '/">' + str(new.news_title) + '</a><br>'
			tree = tree + '</div><a href="/wiki/news/1/' + str(category.id) + '/"><b>More...</b></a> <a href="/wiki/feeds/latestnewsbycategory/' + str(category.id) + '/"><img src="/site_media/wiki/img/rss.png" alt="News from this category as a RSS Feed"></a>'
		text = text.replace(i['tag'], tree)
	return text
