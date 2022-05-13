from django.contrib import admin
from .models import Transaction#, Fee





#------------------------------------------------------------------------------
#class FeeInline(admin.TabularInline):
    #model = Fee
    #extra = 1
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'type', 'status', 'created_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ['source', 'destination']
    #inlines = [FeeInline]
admin.site.register(Transaction, TransactionAdmin)
