def render(dic, text):
	s = 1
	for i in dic:
		text = text.replace(i['tag'], '<a name="' + str(s) +'" href="' +  i['attributes']['id'] + '" title="' + i['code'] + '"></a><h2 style="margin:5px;">' + i['code'] + '</h2>')
		s = s+1
	return text
