from django.contrib import admin
from .models import Transaction, WithdrawalCeiling





#------------------------------------------------------------------------------
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('destination', 'source', 'amount', 'type', 'status', 'created_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ['source', 'destination']
admin.site.register(Transaction, TransactionAdmin)









#------------------------------------------------------------------------------

class WithdrawalCeilingAdmin(admin.ModelAdmin):
    list_display = ('monthly', 'daily')
admin.site.register(WithdrawalCeiling, WithdrawalCeilingAdmin)
