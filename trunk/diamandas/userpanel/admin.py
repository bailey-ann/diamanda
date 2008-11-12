# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from diamandas.userpanel.models import * 

class OpenIdAssociationAdmin(admin.ModelAdmin):
	list_display = ('openid', 'user')

admin.site.register(OpenIdAssociation, OpenIdAssociationAdmin)
