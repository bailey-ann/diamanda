from os.path import isfile
from django.conf import settings

def render(dic, text):
	for i in dic:
		if isfile(settings.SITE_IMAGES_DIR_PATH+i['attributes']['src']):
			thumb = 'thumb_' + i['attributes']['src'];
			if not isfile(settings.SITE_IMAGES_DIR_PATH+thumb):
				import Image
				im = Image.open(settings.SITE_IMAGES_DIR_PATH+i['attributes']['src'])
				im.thumbnail((120, 120))
				im.save(settings.SITE_IMAGES_DIR_PATH+thumb)
		text = text.replace(i['tag'], '<a href="' + settings.SITE_IMAGES_SRC_PATH + i['attributes']['src'] + '" onClick="window.open(\'\',\'popup\', \'height=auto, width=auto, scrollbars=yes, location=no, statusbar=no, resizable=no toolbar=no, menubar=no\')" target="popup"><img src="' + settings.SITE_IMAGES_SRC_PATH + thumb + '" border="0" alt="' + i['attributes']['src'] + '"><br>[ Click on the thumb ]</a>')
	return text
