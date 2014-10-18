from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import *

admin.site.register(Page,MPTTModelAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display  = ['page','value_name']
admin.site.register(Content,ContentAdmin)




