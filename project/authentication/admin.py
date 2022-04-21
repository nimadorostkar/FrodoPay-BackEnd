from django.contrib import admin
from .models import User





#------------------------------------------------------------------------------
class UserAdmin(admin.ModelAdmin):
    list_display = ('img', 'email', 'last_login', 'date_joined', 'is_superuser')
    list_filter = ('date_joined', 'is_active')
    search_fields = ['email', 'firs_name', 'last_name', 'shop']
admin.site.register(User, UserAdmin)
