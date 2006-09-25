def render(dic, text):
	for i in dic:
		if i['attributes'].has_key('desc'):
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/browser.png" alt="" /> <a href="' + i['attributes']['href'] + '/" target="_blank">' + i['code'] + '</a> - '+ i['attributes']['desc'] + '<br />')
		else:
			text = text.replace(i['tag'], '<img src="/site_media/wiki/img/browser.png" alt="" /> <a href="' + i['attributes']['href'] + '/" target="_blank">' + i['code'] + '</a><br />')
	return text
