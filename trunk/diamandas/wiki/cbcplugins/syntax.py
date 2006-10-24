import base64
try:
	from pygments import highlight
	from pygments.lexers import PythonLexer
	from pygments.formatters import HtmlFormatter
except:
	raise Exception, 'No Pygments library! Install pygments from http://pygments.pocoo.org/'
	print 'No Pygments library! Install pygments from http://pygments.pocoo.org/'

def render(dic, text):
	#dp.syntaxhighlighter 1.4.1
	# w3c will kill us for this
	langs = {}
	for i in dic:
		code = base64.b64decode(i['code'])
		text = text.replace(i['tag'], highlight(code, PythonLexer(), HtmlFormatter(linenos=True)))
	text = text + '<style>' + HtmlFormatter().get_style_defs('.highlight') + '</style>'
	return text
