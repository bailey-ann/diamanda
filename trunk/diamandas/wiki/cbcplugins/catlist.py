from wiki.models import *
def render(dic, text):
	for i in dic:
		category = Category.objects.get(cat_name=i['attributes']['name'])
		tree = '<br><img src="/site_media/wiki/img/category.png"> <b>' + i['attributes']['name'] + '</b>'
		if category.cat_description:
			tree = tree + ' - ' + str(category.cat_description)
		pages = category.page_set.all()
		if len(pages) > 0:
			tree = tree +'<div style="padding-left:5px; padding-bottom:3px;">'
			for page in pages:
				tree = tree + '<img src="/site_media/wiki/img/2.png"> <a href="/wiki/page/'+str(page.slug)+'/">' + str(page.title) + '</a> - ' + str(page.description) + '<br>'
			tree = tree + '</div>'
		categories = category.category_set.all()
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
		text = text.replace(i['tag'], tree)
	return text
