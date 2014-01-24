import reversion

from django.contrib import admin

from .models import *


class HaaretzImageline(admin.TabularInline):
    model = HaaretzImage
    fields = ('caption', 'image')


class HaaretzArticleAdmin(reversion.VersionAdmin):
    inlines = (HaaretzImageline,)


admin.site.register(HaaretzArticle, HaaretzArticleAdmin)
admin.site.register(HaaretzImage)
admin.site.register(NewsDiffUser)
