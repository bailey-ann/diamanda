#!/usr/bin/python
# Diamanda Application Set
# Pages module
from string import Template

from django.utils.translation import ugettext as _
from django.template import Context, loader
from django.conf import settings

from diamandas.myghtyboard.templatetags.fbc import fbc
from diamandas.cbcplugins import cbcparser
from diamandas.utils import *

class FeedUpdate:
	"""
	Generates "what's new" list and saves in database for later use
	"""
	def __init__(self, site_id):
		self.feed = []
		self.lastuser = False
		self.r = False
		self.stripper = Stripper()
		self.site_id = site_id
		
		self.rss_feed = []
		self.rss_row = False
		
		self.__make_feed()
	def __make_feed(self):
		"""
		the main method that execute all the code
		"""
		from django.db import connection
		cursor = connection.cursor()
		query = Template("""
			SELECT
				'content', auth_user.username, date, title, description, is_update, changes, slug, content_type, author_id, Null, Null, Null
					FROM rk_content$sid JOIN auth_user ON author_id = auth_user.id WHERE slug != 'index'
			UNION ALL
			SELECT
				'post', rk_post$sid.author, rk_post$sid.date, rk_topic$sid.name, rk_post$sid.text, rk_topic$sid.posts, is_locked, rk_topic$sid.last_pagination_page,
				rk_post$sid.topic_id, rk_topic$sid.is_solved, rk_topic$sid.is_external, rk_post$sid.author_anonymous, rk_post$sid.author_system_id FROM rk_post$sid
					JOIN rk_topic$sid ON rk_post$sid.topic_id = rk_topic$sid.id
			ORDER BY date DESC LIMIT 15""")
		query = query.substitute(sid=int(self.site_id))
		cursor.execute(query)
		rows = cursor.fetchall()
		
		for i in rows:
			self.r = False
			self.rss_row = False
			# handle posts
			if i[0] == 'post' and i[6] != 1:
				self.__handle_post_feed(author=i[1], date=i[2], name=i[3], text=i[4], posts=i[5], is_locked=i[6], last_pagination_page=i[7], topic_id=i[8],
								is_solved=i[9], is_external=i[10], author_anonymous=i[11], author_system_id=i[12])
				self.__rss_handle_post_feed(date=i[2], title=i[3], description=i[4], pagination_page=i[7],topic_id=i[8],is_external=i[10],posts=i[5],is_solved=i[9])
			#handle content
			elif i[0] == 'content':
				self.__handle_content_feed(username=i[1], date=i[2], title=i[3], description=i[4], is_update=i[5], changes=i[6], slug=i[7],
									content_type=i[8], author_id=i[9])
				self.__rss_handle_content_feed(date=i[2], title=i[3], description=i[4],slug=i[7],is_update=i[5], changes=i[6])
			
			if self.r:
				self.feed.append(self.r)
			if self.rss_row:
				self.rss_feed.append(self.rss_row)
	
		ff = ''
		for i in self.feed:
			ff += '<dl>%s</dl>' % i
		self.feed = ff
		
		
		t = loader.get_template('feed/rss.html')
		c = Context({
			'rss': self.rss_feed,
			'domain': settings.SITE_DOMAIN,
			'site_name': settings.SITE_NAME,
			'site_desc': settings.SITE_DESCRIPTION,
			'site_lang': settings.LANGUAGE_CODE,
		})
		self.rss_feed = t.render(c)
		
		from diamandas.pages.models import Feed
		try:
			f = Feed.objects.get(site=self.site_id)
		except:
			f = Feed(site=self.site_id, html=self.feed, rss=self.rss_feed)
			f.save()
		else:
			f.html = self.feed
			f.rss = self.rss_feed
			f.save()
		return True
	
	
	def __handle_post_feed(self, author,date,name,text,posts,is_locked,last_pagination_page,topic_id,is_solved,is_external,author_anonymous,author_system_id):
		"""
		Parse a Post entry
		"""
		if text.find(_('This is a discussion about article')) != -1:
			return True
		text = self.stripper.strip(text.strip().split('\n')[0])
		if len(text) < 10:
			text = ''
		if len(text) > 200 and text.find('[quote]') == -1:
			text = '%s...' % text[0:200]
		elif text.find('[quote]') != -1:
			text = ''
		
		cssclass = 'forum'
		if is_external == 1:
			prefix  = ''
		elif posts > 1:
			prefix  = 'Re: '
		elif is_solved == 1:
			prefix  = _('Solved: ')
		else:
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
				'text': fbc(text),
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
				'text': fbc(text),
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
			cssclass = 'art'
		else:
			text = cbcparser.parse_cbc_tags(description.strip().split('\n')[0])
			cssclass = 'art'
		
		if content_type == 'news':
			cssclass = 'news'
		
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
	
	
	def __rss_handle_content_feed(self, date,title,description,slug,is_update,changes):
		"""
		Handle RSS entries for Content objects
		"""
		t = loader.get_template('feed/content_rss.html')
		c = Context({
			'date': date,
			'title': title,
			'description': cbcparser.parse_cbc_tags(description),
			'slug': slug,
			'is_update':is_update,
			'changes':changes,
			'domain': settings.SITE_DOMAIN
		})
		self.rss_row = t.render(c)
	
	
	def __rss_handle_post_feed(self, date,title,description,pagination_page,topic_id,is_external,posts,is_solved):
		"""
		Handle RSS entries for Post objects
		"""
		if is_external == 1:
			prefix  = ''
		elif posts > 1:
			prefix  = 'Re: '
		elif is_solved == 1:
			prefix  = _('Solved: ')
		else:
			prefix  = ''
		
		t = loader.get_template('feed/forum_rss.html')
		c = Context({
			'date': date,
			'title': title,
			'description': fbc(description),
			'pagination_page': pagination_page,
			'topic_id':topic_id,
			'prefix': prefix,
			'domain': settings.SITE_DOMAIN
		})
		self.rss_row = t.render(c)
