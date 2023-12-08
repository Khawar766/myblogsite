
# Register your models here.
from django.contrib import admin
from .models import Blogpost,Blogcomment, Contact
admin.site.register(Contact)
admin.site.register(Blogcomment)
@admin.register(Blogpost)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',)