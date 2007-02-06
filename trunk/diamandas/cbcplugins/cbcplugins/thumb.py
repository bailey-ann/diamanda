from os.path import isfile
from django.conf import settings

def render(dic, text):
	for i in dic:
		img = i['attributes']['src'].split('/')
		thumb = 'thumb_' + img[-1]
		im = img[-1]
		domain = img[0]
		if isfile(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + im):
			if not isfile(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + thumb):
				import Image
				imi = Image.open(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + im)
				imi.thumbnail((120, 120))
				imi.save(settings.MEDIA_ROOT + 'resources/' + domain + '.rk.edu.pl/images/' + thumb)
			text = text.replace(i['tag'], '<div style="text-align:center;"><a href="/site_media/resources/' + domain + '.rk.edu.pl/images/' + im + '" onClick="return enlarge(\'/site_media/resources/' + domain + '.rk.edu.pl/images/' + im + '\',event, \'center\', 520, 520)"><img src="/site_media/resources/' + domain + '.rk.edu.pl/images/' + thumb + '" alt="' + im + '" /></a></div>')
	return text

def describe():
	return {'tag':'thumb', 'tag_example':_('[rk:thumb src="image.jpg"] [rk:thumb src="folder/image.jpg"]'), 'description':_('Will insert a link to a local image using a thumb and a pop-up. The thumb will be created by PIL. Images can be in SITE_IMAGES_DIR_PATH subfolders.')}
