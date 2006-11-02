try:
	from pygments import highlight
	from pygments.lexers import *
	from pygments.formatters import HtmlFormatter
except:
	raise Exception, 'No Pygments library! Install pygments from http://pygments.pocoo.org/'
	print 'No Pygments library! Install pygments from http://pygments.pocoo.org/'

def render(dic, text):
	langs = {}
	for i in dic:
		if i['attributes']['lang'] == 'python':
			text = text.replace(i['tag'], highlight(i['code'], PythonLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'xml':
			text = text.replace(i['tag'], highlight(i['code'], XmlLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'html':
			text = text.replace(i['tag'], highlight(i['code'], HtmlLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'ruby':
			text = text.replace(i['tag'], highlight(i['code'], RubyLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'perl':
			text = text.replace(i['tag'], highlight(i['code'], PerlLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'lua':
			text = text.replace(i['tag'], highlight(i['code'], LuaLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'cpp':
			text = text.replace(i['tag'], highlight(i['code'], CppLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'delphi':
			text = text.replace(i['tag'], highlight(i['code'], DelphiLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'java':
			text = text.replace(i['tag'], highlight(i['code'], JavaLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'php':
			text = text.replace(i['tag'], highlight(i['code'], PhpLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'makefile':
			text = text.replace(i['tag'], highlight(i['code'], MakefileLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'diff':
			text = text.replace(i['tag'], highlight(i['code'], DiffLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'javascript':
			text = text.replace(i['tag'], highlight(i['code'], JavascriptLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'css':
			text = text.replace(i['tag'], highlight(i['code'], CssLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'sql':
			text = text.replace(i['tag'], highlight(i['code'], SqlLexer(), HtmlFormatter()))
		else:
			text = text.replace(i['tag'], highlight(i['code'], HtmlLexer(), HtmlFormatter()))

	text = text + '<style>' + HtmlFormatter().get_style_defs('.highlight') + '</style>'
	return text
