from django.contrib import admin
from .models import User, Countries, NotifLists
from import_export.admin import ImportExportModelAdmin, ImportExportMixin










#------------------------------------------------------------------------------
class CountriesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'flagImg', 'available')
    list_filter = ('available',)
    search_fields = ['name',]
admin.site.register(Countries, CountriesAdmin)






#------------------------------------------------------------------------------
class UserAdmin(admin.ModelAdmin):
    list_display = ('img', 'username', 'email', 'country', 'flag', 'inventory', 'date_joined')
    list_filter = ('date_joined', 'is_active', 'country', 'inventory')
    raw_id_fields = ('country'),
    search_fields = ['email', 'firs_name', 'last_name', 'shop']
admin.site.register(User, UserAdmin)








#------------------------------------------------------------------------------
class NotifListsAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'type', 'user')
    list_filter = ('time', 'type', 'user')
admin.site.register(NotifLists, NotifListsAdmin)










#End
