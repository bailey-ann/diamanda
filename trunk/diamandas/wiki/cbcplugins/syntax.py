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
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], PythonLexer(), HtmlFormatter(cssclass='highlight_py')) + '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_py') + '</style>'] = True
		elif i['attributes']['lang'] == 'xml':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], XmlLexer(), HtmlFormatter(cssclass='highlight_html'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_html') + '</style>'] = True
		elif i['attributes']['lang'] == 'html':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], HtmlLexer(), HtmlFormatter(cssclass='highlight_html'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_html') + '</style>'] = True
		elif i['attributes']['lang'] == 'ruby':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], RubyLexer(), HtmlFormatter(cssclass='highlight_rb'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_rb') + '</style>'] = True
		elif i['attributes']['lang'] == 'perl':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], PerlLexer(), HtmlFormatter(cssclass='highlight_pl'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_pl') + '</style>'] = True
		elif i['attributes']['lang'] == 'lua':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], LuaLexer(), HtmlFormatter(cssclass='highlight_lua'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_lua') + '</style>'] = True
		elif i['attributes']['lang'] == 'cpp':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], CppLexer(), HtmlFormatter(cssclass='highlight_cpp'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_cpp') + '</style>'] = True
		elif i['attributes']['lang'] == 'delphi':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], DelphiLexer(), HtmlFormatter(cssclass='highlight_delphi'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_delphi') + '</style>'] = True
		elif i['attributes']['lang'] == 'java':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], JavaLexer(), HtmlFormatter(cssclass='highlight_java'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_java') + '</style>'] = True
		elif i['attributes']['lang'] == 'php':
			if i['code'].find('<?') == -1:
				i['code'] = '<?php\n' + i['code']
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], PhpLexer(), HtmlFormatter(cssclass='highlight_php'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_php') + '</style>'] = True
		elif i['attributes']['lang'] == 'makefile':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], MakefileLexer(), HtmlFormatter(cssclass='highlight_make'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_make') + '</style>'] = True
		elif i['attributes']['lang'] == 'diff':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], DiffLexer(), HtmlFormatter(cssclass='highlight_diff'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_diff') + '</style>'] = True
		elif i['attributes']['lang'] == 'javascript':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], JavascriptLexer(), HtmlFormatter(cssclass='highlight_js'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_js') + '</style>'] = True
		elif i['attributes']['lang'] == 'css':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], CssLexer(), HtmlFormatter(cssclass='highlight_css'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_css') + '</style>'] = True
		elif i['attributes']['lang'] == 'sql':
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], SqlLexer(), HtmlFormatter(cssclass='highlight_sql'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_sql') + '</style>'] = True
		else:
			text = text.replace(i['tag'], '<div class="box" style="overflow:auto;font-size:10px;">' + highlight(i['code'], HtmlLexer(), HtmlFormatter(cssclass='highlight_html'))+ '</div>')
			langs['<style>' + HtmlFormatter().get_style_defs('.highlight_html') + '</style>'] = True
	keys = str(langs.keys()).replace("['", '').replace("']", '')
	text = text + keys.replace('\\n', '''
''')
	return text
