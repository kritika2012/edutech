from django.contrib import admin
from app.models import Post,Comment,teacher

class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','updated','status']
    list_filter=('status','author','created','publish')
    search_fields=('title','body')
    date_hierarchy='publish'
    ordering=['status','publish']
    prepopulated_fields={'slug':('title',)}

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(teacher)
