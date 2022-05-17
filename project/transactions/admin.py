from django.contrib import admin
from .models import Transaction





#------------------------------------------------------------------------------

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'type', 'status', 'created_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ['source', 'destination']
admin.site.register(Transaction, TransactionAdmin)
