#!/usr/bin/python
# Diamanda Application Set
# Pages module
from string import Template

from django.utils.translation import ugettext as _
from django.template import Context, loader
from utils import *

class FeedUpdate():
	def __init__(self, site_id):
		self.feed = []
		self.lastuser = False
		self.r = False
		self.stripper = Stripper()
		self.site_id = site_id
		self.__make_feed()
	def __make_feed(self):
		"""
		Generates "what's new" list and saves in database for later use
		
		site_id - ID of the site defined in settings.py as SITE_ID
		"""
		from django.db import connection
		cursor = connection.cursor()
		query = Template("""
			SELECT
				'content', auth_user.username, date, title, description, is_update, changes, slug, content_type, author_id, Null, Null, Null
					FROM rk_content$sid JOIN auth_user ON author_id = auth_user.id
			UNION ALL
			SELECT
				'topic', rk_post$sid.author, rk_post$sid.date, rk_topic$sid.name, rk_post$sid.text, rk_topic$sid.posts, is_locked, rk_topic$sid.last_pagination_page,
				rk_post$sid.topic_id, rk_topic$sid.is_solved, rk_topic$sid.is_external, rk_post$sid.author_anonymous, rk_post$sid.author_system_id FROM rk_post$sid
					JOIN rk_topic$sid ON rk_post$sid.topic_id = rk_topic$sid.id
			ORDER BY date DESC LIMIT 15""")
		query = query.substitute(sid=int(self.site_id))
		cursor.execute(query)
		rows = cursor.fetchall()
		
		for i in rows:
			self.r = False
			# handle posts
			if i[0] == 'topic' and i[6] != 1:
				self.__handle_post_feed(author=i[1], date=i[2], name=i[3], text=i[4], posts=i[5], is_locked=i[6], last_pagination_page=i[7], topic_id=i[8],
								is_solved=i[9], is_external=i[10], author_anonymous=i[11], author_system_id=i[12])
			#handle content
			elif i[0] == 'content':
				self.__handle_content_feed(username=i[1], date=i[2], title=i[3], description=i[4], is_update=i[5], changes=i[6], slug=i[7],
									content_type=i[8], author_id=i[9])
			
			if self.r:
				self.feed.append(self.r)
	
		ff = ''
		for i in self.feed:
			ff += '<div class="feed">%s</div>' % i
		self.feed = ff
		
		from pages.models import Feed
		try:
			f = Feed.objects.get(site=self.site_id)
		except:
			f = Feed(site=site_id, text=self.feed)
			f.save()
		else:
			f.text = self.feed
			f.save()
		return True
	def __handle_post_feed(self, author,date,name,text,posts,is_locked,last_pagination_page,topic_id,is_solved,is_external,author_anonymous,author_system_id,):
		"""
		Parse a Post entry
		"""
		text = self.stripper.strip(text.strip().split('\n')[0])
		if len(text) > 200:
			text = '%s...' % text[0:200]
		
		if is_external == 1:
			prefix  = ''
			cssclass = 'reply_feed'
		elif posts > 1:
			cssclass = 'reply_feed'
			prefix  = 'Re: '
		elif is_solved == 1:
			cssclass = 'forum_feed'
			prefix  = _('Solved: ')
		else:
			cssclass = 'forum_feed'
			prefix  = ''
		# append entry to current user DIV block
		if self.lastuser and self.lastuser == author:
			t = loader.get_template('feed/forum_insert.html')
			c = Context({
				'cssclass': cssclass,
				'pagination_page': last_pagination_page,
				'topic_id': topic_id,
				'prefix': prefix,
				'topic_title': self.stripper.strip(name),
				'text': text,
				'author_anonymous': author_anonymous
			})
			appended = t.render(c)
	
			self.feed[-1] = self.feed[-1].replace('<!-- -->', appended)
			# make a new block for a new user
		else:
			t = loader.get_template('feed/forum_block.html')
			c = Context({
				'user_id': author_system_id,
				'username': author[0:14],
				'date': date[:10],
				'cssclass': cssclass,
				'pagination_page': last_pagination_page,
				'topic_id': topic_id,
				'prefix': prefix,
				'topic_title': self.stripper.strip(name),
				'text': text,
				'author_anonymous': author_anonymous
			})
			self.r = t.render(c)
		self.lastuser = author
		return True
	
	def __handle_content_feed(self, username,date,title,description,is_update,changes,slug,content_type,author_id):
		"""
		Parse a Content entry
		"""
		if is_update == 1:
			text = self.stripper.strip(changes)
			cssclass = 'content_update_feed'
		else:
			text = self.stripper.strip(description.strip().split('\n')[0])
			if len(text) > 200:
				text = '%s...' % text[0:200]
			cssclass = 'content_feed'
		
		if content_type == 'news':
			cssclass = 'news_feed'
		
		# append entry to current user DIV block
		if self.lastuser and self.lastuser == username:
			t = loader.get_template('feed/content_insert.html')
			c = Context({
				'cssclass': cssclass,
				'slug': slug,
				'title': self.stripper.strip(title),
				'text': text
			})
			appended = t.render(c)
			self.feed[-1] = self.feed[-1].replace('<!-- -->', appended)
		# make a new block for a new user
		else:
			t = loader.get_template('feed/content_block.html')
			c = Context({
				'user_id': author_id,
				'username': username[0:14],
				'date': date[:10],
				'cssclass': cssclass,
				'slug': slug,
				'title': self.stripper.strip(title),
				'text': text
			})
			self.r = t.render(c)
		self.lastuser = username
		return True