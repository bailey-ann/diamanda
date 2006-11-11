from os.path import isfile
from django.conf import settings

def render(dic, text):
	for i in dic:
		if isfile(settings.SITE_IMAGES_DIR_PATH+i['attributes']['src']):
			if i['attributes']['src'].find('/') != -1:
				img = i['attributes']['src'].split('/')
				thumb = 'thumb_' + img[-1]
				thumb = img[0] + '/thumb_' + img[-1]
				print thumb
			else:
				thumb = 'thumb_' + i['attributes']['src']
			if not isfile(settings.SITE_IMAGES_DIR_PATH+thumb):
				import Image
				im = Image.open(settings.SITE_IMAGES_DIR_PATH+i['attributes']['src'])
				im.thumbnail((120, 120))
				im.save(settings.SITE_IMAGES_DIR_PATH+thumb)
		text = text.replace(i['tag'], '<div style="text-align:center;"><a href="' + settings.SITE_IMAGES_SRC_PATH + i['attributes']['src'] + '" onClick="window.open(\'\',\'popup\', \'height=auto, width=auto, scrollbars=yes, location=no, statusbar=no, resizable=no toolbar=no, menubar=no\')" target="popup"><img src="' + settings.SITE_IMAGES_SRC_PATH + thumb + '" alt="' + i['attributes']['src'] + '" /></a></div>')
	return text

def describe():
	return {'tag':'thumb', 'tag_example':_('[rk:thumb src="image.jpg"] [rk:thumb src="folder/image.jpg"]'), 'description':_('Will insert a link to a local image using a thumb and a pop-up. The thumb will be created by PIL. Images can be in SITE_IMAGES_DIR_PATH subfolders.')}
