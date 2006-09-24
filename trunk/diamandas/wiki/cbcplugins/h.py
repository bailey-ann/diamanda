def render(dic, text):
	s = 1
	for i in dic:
		text = text.replace(i['tag'], '<a name="' + str(s) +'" href="' +  i['attributes']['id'] + '" title="' + i['code'] + '"></a><h'+ i['attributes']['id'] +' class="pageh">' + i['code'] + '</h'+ i['attributes']['id'] +'>')
		s = s+1
	return text
