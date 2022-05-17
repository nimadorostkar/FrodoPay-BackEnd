from django.contrib import admin
from .models import User, Countries
from import_export.admin import ImportExportModelAdmin, ImportExportMixin










#------------------------------------------------------------------------------
class CountriesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'flagImg', 'available')
    list_filter = ('available',)
    search_fields = ['name',]
admin.site.register(Countries, CountriesAdmin)






#------------------------------------------------------------------------------
class UserAdmin(admin.ModelAdmin):
    list_display = ('img', 'username', 'email', 'country', 'flag', 'date_joined', 'is_superuser')
    list_filter = ('date_joined', 'is_active', 'country')
    raw_id_fields = ('country'),
    search_fields = ['email', 'firs_name', 'last_name', 'shop']
admin.site.register(User, UserAdmin)
