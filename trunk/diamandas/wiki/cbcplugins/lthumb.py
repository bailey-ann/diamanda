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
		text = text.replace(i['tag'], '<div style="text-aling:center;"><a href="' + settings.SITE_IMAGES_SRC_PATH + i['attributes']['src'] + '" rel="lightbox"><img src="' + settings.SITE_IMAGES_SRC_PATH + thumb + '" alt="' + i['attributes']['src'] + '" /></a></div>')
		text = '<script type="text/javascript" src="/site_media/cbc/lthumb/js/lightbox.js"></script><link rel="stylesheet" href="/site_media/cbc/lthumb/css/lightbox.css" type="text/css" media="screen" />' + text
	return text
