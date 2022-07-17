from django.contrib import admin
from .models import Advertise










#------------------------------------------------------------------------------
class AdvertiseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Img', 'link')
admin.site.register(Advertise, AdvertiseAdmin)
