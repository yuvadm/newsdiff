import reversion

from django.contrib import admin

from .models import *


class HaaretzImageline(admin.TabularInline):
    model = HaaretzImage
    fields = ('caption', 'image')


class HaaretzArticleAdmin(reversion.VersionAdmin):
    inlines = (HaaretzImageline,)


class YnetImageline(admin.TabularInline):
    model = YnetImage
    fields = ('caption', 'image')


class YnetArticleAdmin(reversion.VersionAdmin):
    inlines = (YnetImageline,)


admin.site.register(HaaretzArticle, HaaretzArticleAdmin)
admin.site.register(HaaretzImage)
admin.site.register(YnetArticle, YnetArticleAdmin)
admin.site.register(YnetImage)
admin.site.register(NewsDiffUser)
