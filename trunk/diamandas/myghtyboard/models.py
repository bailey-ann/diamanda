from django.db import models
#from django.conf import settings

# Forum Categories
class Category(models.Model):
	cat_name = models.CharField(maxlength=255, verbose_name="Category Name") # name of the category
	cat_order = models.PositiveSmallIntegerField(default=0, verbose_name="Order") # order of categories on the forum-categories list
	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"
		#db_table = 'rk_category' + str(settings.SITE_ID)
	class Admin:
		list_display = ('cat_name','cat_order')
	def __str__(self):
		return self.cat_name

# Forums
class Forum(models.Model):
	forum_category = models.ForeignKey(Category, verbose_name="Forum Category") # Forum category
	forum_name = models.CharField(maxlength=255, verbose_name="Forum Name") # name of the forum
	forum_description = models.CharField(maxlength=255, verbose_name="Forum Description") # desc of the forum
	forum_topics = models.PositiveIntegerField(default='0', blank=True, verbose_name="Topics") # number of topics
	forum_posts = models.PositiveIntegerField(default='0', blank=True, verbose_name="Posts") # number of posts
	forum_lastpost = models.CharField(maxlength=255, verbose_name="Last Post", blank=True, default='', null=True) # last poster info etc.
	forum_order = models.PositiveSmallIntegerField(default=0) # order of forums on the category list
	class Meta:
		verbose_name = "Forum"
		verbose_name_plural = "Forums"
		#db_table = 'rk_forum' + str(settings.SITE_ID)
	class Admin:
		list_display = ('forum_name', 'forum_description', 'forum_category', 'forum_order')
		fields = (
		(None, {
		'fields': ('forum_category', 'forum_name', 'forum_description', 'forum_order')
		}),)
	def __str__(self):
		return self.forum_name

# Topics
class Topic(models.Model):
	topic_forum = models.ForeignKey(Forum, verbose_name="Forum") # Forum of the topic
	topic_name = models.CharField(maxlength=255, verbose_name="Topic Title") # name of the topic
	topic_author = models.CharField(maxlength=255, verbose_name="Author", blank=True) # topic author
	topic_posts = models.PositiveIntegerField(default=0, blank=True, verbose_name="Posts") # number of posts
	topic_lastpost = models.CharField(maxlength=255, verbose_name="Last Post") # last poster etc.
	topic_modification_date = models.DateTimeField(auto_now = True) # last post date :)
	is_sticky = models.BooleanField(blank=True, default=False)
	is_locked = models.BooleanField(blank=True, default=False)
	is_global = models.BooleanField(blank=True, default=False)
	class Meta:
		verbose_name = "Topic"
		verbose_name_plural = "Topics"
		#db_table = 'rk_topic' + str(settings.SITE_ID)
	def __str__(self):
		return self.topic_name

class Post(models.Model):
	post_topic = models.ForeignKey(Topic, verbose_name="Post")
	post_text = models.TextField() # the post text
	post_author = models.CharField(maxlength=255, verbose_name="Author", blank=True) # topic author
	post_date = models.DateTimeField(auto_now_add = True) # post add date
	post_ip = models.CharField(maxlength=20, blank=True)
	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"
		#db_table = 'rk_post' + str(settings.SITE_ID)
	def __str__(self):
		return str(self.id)
