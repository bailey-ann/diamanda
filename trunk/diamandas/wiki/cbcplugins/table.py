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
