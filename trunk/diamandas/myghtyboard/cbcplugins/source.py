def render(dic, text):
	#dp.syntaxhighlighter 1.4.0
	import base64
	for i in dic:
		if i['attributes']['lang'] != 'xml':
			i['attributes']['lang'] = 'xml'
		code = base64.b64decode(i['code']).replace('</te', '</ te')
		code = code.replace('</TE', '</ TE')
		code = code.replace('</Te', '</ Te')
		code = code.replace('</tE', '</ tE')
		text = text.replace(i['tag'], '<textarea name="code" class="'+ i['attributes']['lang'] +'" rows="15" cols="90">' + code + '</textarea>')
	return text
