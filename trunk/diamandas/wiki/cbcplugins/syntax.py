import base64
def render(dic, text):
	#dp.syntaxhighlighter 1.4.1
	# w3c will kill us for this
	text = '<link type="text/css" rel="stylesheet" href="/site_media/cbc/syntax/Styles/SyntaxHighlighter.css" media="screen"></link>' + text
	langs = {}
	for i in dic:
		code = base64.b64decode(i['code']).replace('</te', '</ te')
		code = code.replace('</TE', '</ TE')
		code = code.replace('</Te', '</ Te')
		code = code.replace('</tE', '</ tE')
		text = text.replace(i['tag'], '<textarea name="code" class="'+ i['attributes']['lang'] +'" rows="15" cols="90">' + code + '</textarea>')
		# what langs are used?
		langs[i['attributes']['lang']] = True
	
	# add the core JS
	text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shCore.js"></script>'
	# add only those lang-JS files that we realy need. For example i limit it to two
	if langs.has_key('python'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushPython.js"></script>'
	if langs.has_key('xml'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushXml.js"></script>'
	if langs.has_key('csharp'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushCSharp.js"></script>'
	if langs.has_key('php'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushPhp.js"></script>'
	if langs.has_key('js'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushJScript.js"></script>'
	if langs.has_key('java'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushJava.js"></script>'
	if langs.has_key('vb'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushVb.js"></script>'
	if langs.has_key('sql'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushSql.js"></script>'
	if langs.has_key('delphi'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushDelphi.js"></script>'
	if langs.has_key('ruby'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushRuby.js"></script>'
	if langs.has_key('css'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushCss.js"></script>'
	if langs.has_key('cpp'):
		text = text + '<script type="text/javascript" src="/site_media/cbc/syntax/Scripts/shBrushCpp.js"></script>'
	# the end, activate the code
	return text + '<script class="javascript">dp.SyntaxHighlighter.HighlightAll(\'code\');</script>'
