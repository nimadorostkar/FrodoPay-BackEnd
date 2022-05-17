from django.contrib import admin
from .models import User, Countries









#------------------------------------------------------------------------------
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'flagImg', 'available')
    list_filter = ('available',)
    search_fields = ['name',]
admin.site.register(Countries, CountriesAdmin)




#------------------------------------------------------------------------------
class UserAdmin(admin.ModelAdmin):
    list_display = ('img', 'username', 'email', 'last_login', 'date_joined', 'is_superuser')
    list_filter = ('date_joined', 'is_active')
    search_fields = ['email', 'firs_name', 'last_name', 'shop']
admin.site.register(User, UserAdmin)
