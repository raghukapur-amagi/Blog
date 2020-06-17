from django.contrib import admin

# Register your models here.

from .models import Articles, Tags, ArticleTagMapping, Comments

admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(ArticleTagMapping)
admin.site.register(Comments)