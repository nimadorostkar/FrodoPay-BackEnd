from django.contrib import admin
from .models import Transaction





#------------------------------------------------------------------------------
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ['wallet__wallet_id']
    raw_id_fields = ('wallet'),
admin.site.register(Transaction, TransactionAdmin)
