from django.contrib import admin
from .models import Category,Tag,BlogPost

# Register your models here.
    
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title','timestamp','updated','category',]
    #def category(self,obj):
    #    return str(obj.category.name)

    
class Admin(admin.ModelAdmin):
    list_display = ['name',]
    
admin.site.register(Category,Admin)
admin.site.register(Tag,Admin)
admin.site.register(BlogPost,BlogPostAdmin)
