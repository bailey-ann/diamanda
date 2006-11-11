def render(dic, text):
	td = '</td><td>'
	for i in dic:
		ret = ''
		first = False
		for line in i['code'].split('\n'):
			if len(line) > 1:
				columns = line.split('|')
				if not first:
					ret = '<thead><tr><td>' + td.join(columns) + '</td></tr></thead><tbody>'
					first = True
				else:
					ret = ret + '<tr><td>' + td.join(columns) + '</td></tr>'
		if i['attributes'].has_key('width'):
			width = i['attributes']['width']
		else:
			width = '100%'
		text = text.replace(i['tag'], '<table id="' + i['attributes']['name'] + '" width="' + width + '" align="center">' + ret + '</tbody></table><script type="text/javascript">addTableRolloverEffect(\'' + i['attributes']['name'] + '\', \'tableRollOverEffect1\');initSortTable(\'' + i['attributes']['name'] + '\',Array(' + i['attributes']['sort'] + '));</script>')
	text = '<script language="JavaScript" src="/site_media/cbc/table/table.js" charset="utf-8"></script><link rel="stylesheet" href="/site_media/cbc/table/table.css" type="text/css" media="screen" />' + text
	return text


def describe():
	return {'tag':'table', 'tag_example':_('''[rk:table name="tablea" width="50%" sort="'N', 'S', 'S'"]
field1|field2|fiel3
1|valuex|valuey
4|bar|text
2|tekx2|foo
[/rk:table]'''), 'description':_('Will insert a table with row highlighting and column sorting. name - unique name for each table on the page, width - optional, default 100%, sort - defines sorting rules, S - string, N - number - for each column. Between tags you place the table structure, using | as a column separator. First row is the table head, the rest is the table data.')}