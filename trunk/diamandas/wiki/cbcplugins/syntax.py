import base64
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
		code = base64.decodestring(i['code'])
		if i['attributes']['lang'] == 'python':
			text = text.replace(i['tag'], highlight(code, PythonLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'xml':
			text = text.replace(i['tag'], highlight(code, XmlLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'html':
			text = text.replace(i['tag'], highlight(code, HtmlLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'ruby':
			text = text.replace(i['tag'], highlight(code, RubyLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'perl':
			text = text.replace(i['tag'], highlight(code, PerlLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'lua':
			text = text.replace(i['tag'], highlight(code, LuaLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'cpp':
			text = text.replace(i['tag'], highlight(code, CppLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'delphi':
			text = text.replace(i['tag'], highlight(code, DelphiLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'java':
			text = text.replace(i['tag'], highlight(code, JavaLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'php':
			text = text.replace(i['tag'], highlight(code, PhpLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'makefile':
			text = text.replace(i['tag'], highlight(code, MakefileLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'diff':
			text = text.replace(i['tag'], highlight(code, DiffLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'javascript':
			text = text.replace(i['tag'], highlight(code, JavascriptLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'css':
			text = text.replace(i['tag'], highlight(code, CssLexer(), HtmlFormatter()))
		elif i['attributes']['lang'] == 'sql':
			text = text.replace(i['tag'], highlight(code, SqlLexer(), HtmlFormatter()))
		else:
			text = text.replace(i['tag'], highlight(code, HtmlLexer(), HtmlFormatter()))
			
			
			
	text = text + '<style>' + HtmlFormatter().get_style_defs('.highlight') + '</style>'
	return text
