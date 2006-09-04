def render(dic, text):
	s = 1
	for i in dic:
		text = text.replace(i['tag'], '<h'+ i['attributes']['id'] +' class="pageh">' + i['code'] + '</h'+ i['attributes']['id'] +'><a name="' + str(s) +'" h="' +  i['attributes']['id'] + '" title="' + i['code'] + '"></a>')
		s = s+1
	return text
