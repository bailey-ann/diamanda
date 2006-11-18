def render(dic, text):
	for i in dic:
		if i['attributes'].has_key('desc'):
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/browser.png" alt="" /> <a href="' + i['attributes']['href'] + '" target="_blank">' + i['code'] + '</a> - '+ i['attributes']['desc'] + '<br />')
		else:
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/browser.png" alt="" /> <a href="' + i['attributes']['href'] + '" target="_blank">' + i['code'] + '</a><br />')
	return text

def describe():
	return {'tag':'link', 'tag_example':_('[rk:link href="URL" desc="DESCRIPTION"]TITLE[/rk:link]'), 'description':_('Will insert a external link with nice icon. "desc" attribute is optional and if added will display a description text by the link')}