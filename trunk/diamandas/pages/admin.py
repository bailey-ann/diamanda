# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from diamandas.pages.models import *

class ContentAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'content_type', 'place')
	list_filter = ['content_type']
	search_fields = ['title', 'slug', 'text']
	prepopulated_fields = {'slug': ('title',)}
	fieldsets = (
		(_('Content'),
			{
			'fields': ('title', 'slug', 'description', 'text', 'content_type','place', 'author')
			}),
		(_('Book'),
			{
			'fields': ('book_order', 'coment_forum')
			}),
		(_('Updates'),
			{
			'fields': ('is_update', 'changes')
			}),
		(_('Content Menu'),
			{
			'fields': ('leftmenu',)
			}),
		)

admin.site.register(Content, ContentAdmin)
