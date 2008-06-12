#!/usr/bin/python
# Diamanda Application Set
# Pages module
from string import Template

from django.utils.translation import ugettext as _
from django.template import Context, loader

def make_feed(site_id = 1):
	"""
	Generates "what's new" list and saves in database for later use
	
	site_id - ID of the site defined in settings.py as SITE_ID
	"""
	from django.db import connection
	cursor = connection.cursor()
	query = Template("""
		SELECT
			'content', auth_user.username, date, title, description, is_update, changes, slug, content_type, Null  FROM rk_content$sid JOIN auth_user ON author_id = auth_user.id
		UNION ALL
		SELECT
			'topic', rk_post$sid.author, rk_post$sid.date, rk_topic$sid.name, rk_post$sid.text, rk_topic$sid.posts, is_locked, rk_topic$sid.last_pagination_page,
			rk_post$sid.topic_id, rk_topic$sid.is_solved FROM rk_post$sid
				JOIN rk_topic$sid ON rk_post$sid.topic_id = rk_topic$sid.id
		ORDER BY date DESC LIMIT 15""")
	query = query.substitute(sid=site_id)
	cursor.execute(query)
	row = cursor.fetchall()
	
	feed = []
	lastuser = False
	for i in row:
		r = False
		# handle new posts
		#'topic' - 0, author - 1, date - 2, name - 3, text - 4, posts - 5, is_locked - 6, last_pagination_page - 7, topic_id - 8, is_solved - 9
		if i[0] == 'topic' and i[6] != 1:
			text = i[4].split('\n')[0]
			if len(text) > 100:
				text = '%s...' % text[0:100]
			
			if i[5] > 1:
				cssclass = 'reply_feed'
				prefix  = 'Re: '
			elif i[9] == 1:
				cssclass = 'forum_feed'
				prefix  = _('Solved: ')
			else:
				cssclass = 'forum_feed'
				prefix  = ''
			# append entry to current user DIV block
			if lastuser and lastuser == i[1]:
				t = loader.get_template('feed/forum_insert.html')
				c = Context({
					'cssclass': cssclass,
					'pagination_page': i[7],
					'topic_id': i[8],
					'prefix': prefix,
					'topic_title': i[3],
					'text': text
				})
				appended = t.render(c)

				feed[-1] = feed[-1].replace('<!-- -->', appended)
			# make a new block for a new user
			else:
				t = loader.get_template('feed/forum_block.html')
				c = Context({
					'user_id': 'ID_USERA_DO_PROFILU',
					'username': i[1],
					'date': i[2][:10],
					'cssclass': cssclass,
					'pagination_page': i[7],
					'topic_id': i[8],
					'prefix': prefix,
					'topic_title': i[3],
					'text': text
				})
				r = t.render(c)
			lastuser = i[1]
		#handle content entries
		#'content' - 0, auth_user.username - 1, date - 2, title - 3, description - 4, is_update - 5, changes - 6, slug - 7, content_type - 8, Null - 9
		elif i[0] == 'content':
			if i[5] == 1:
				text = i[6] # update text
				cssclass = 'content_update_feed'
			else:
				text = i[4].split('\n')[0]
				if len(text) > 100:
					text = '%s...' % text[0:100]
				cssclass = 'content_feed'
			
			if i[8] == 'news':
				cssclass = 'news_feed'
			
			# append entry to current user DIV block
			if lastuser and lastuser == i[1]:
				t = loader.get_template('feed/content_insert.html')
				c = Context({
					'cssclass': cssclass,
					'slug': i[7],
					'title': i[3],
					'text': text
				})
				appended = t.render(c)
				feed[-1] = feed[-1].replace('<!-- -->', appended)
			# make a new block for a new user
			else:
				t = loader.get_template('feed/content_block.html')
				c = Context({
					'user_id': 'ID_USERA_DO_PROFILU',
					'username': i[1],
					'date': i[2][:10],
					'cssclass': cssclass,
					'slug': i[7],
					'title': i[3],
					'text': text
				})
				r = t.render(c)
			
			#update user for DIV appending
			lastuser = i[1]
		if r:
			feed.append(r)
	
	ff = ''
	for i in feed:
		ff += '<div class="feed">%s</div>' % i
	feed = ff
	
	from pages.models import Feed
	try:
		f = Feed.objects.get(site=site_id)
	except:
		f = Feed(site=site_id, text=feed)
		f.save()
	else:
		f.text = feed
		f.save()
	return True