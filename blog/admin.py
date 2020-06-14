from django.contrib import admin

# Register your models here.

from .models import Articles, Tags, Article_Tag_Mapping, Comments

admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Article_Tag_Mapping)
admin.site.register(Comments)