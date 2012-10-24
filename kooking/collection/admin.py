from django.contrib import admin
from fpage.collection.models import *

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id','page_name')

admin.site.register(Collection,CollectionAdmin)
