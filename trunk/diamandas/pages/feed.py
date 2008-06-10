#!/usr/bin/python
# Diamanda Application Set
# Pages module
from django.template import Context, loader

from userpanel.models import Profile
from myghtyboard.models import Topic
from pages.models import Content


def make_feed(site_id = 1):
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute("""
		SELECT
			'content', auth_user.username, date, title, description, is_update, changes, slug, Null  FROM rk_content1 JOIN auth_user ON author_id = auth_user.id
		UNION ALL
		SELECT
			'topic', rk_post1.author, rk_post1.date, rk_topic1.name, rk_post1.text, rk_topic1.posts, is_locked, rk_topic1.last_pagination_page, rk_post1.topic_id FROM rk_post1 JOIN rk_topic1 ON rk_post1.topic_id = rk_topic1.id
		ORDER BY date DESC LIMIT 15""")
	row = cursor.fetchall()
	
	feed = []
	lastuser = False
	for i in row:
		r = False
		if i[0] == 'topic' and i[6] != 1:
			text = i[4].split('\n')[0]
			if len(text) > 100:
				text = '%s...' % text[0:100]
			
			if i[5] > 1:
				cssclass = 'reply_feed'
				prefix  = 'Re: '
			else:
				cssclass = 'forum_feed'
				prefix  = ''
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
		elif i[0] == 'content':
			if i[5] == 1:
				text = i[6] # update text
				cssclass = 'content_update_feed'
			else:
				text = i[4].split('\n')[0]
				if len(text) > 100:
					text = '%s...' % text[0:100]
				cssclass = 'content_feed'
			
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

			lastuser = i[1]
		
		if r:
			feed.append(r)
	
	return feed