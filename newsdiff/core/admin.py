import reversion

from django.contrib import admin

from .models import *


class HaaretzArticleAdmin(reversion.VersionAdmin):
    pass

admin.site.register(HaaretzArticle, HaaretzArticleAdmin)
admin.site.register(NewsDiffUser)
admin.site.register(HaaretzImage)

