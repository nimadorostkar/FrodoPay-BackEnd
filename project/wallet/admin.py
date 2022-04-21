from django.contrib import admin
from .models import Wallet





#------------------------------------------------------------------------------
class WalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_id', 'user', 'inventory', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ['wallet_id']
    raw_id_fields = ('user'),
admin.site.register(Wallet, WalletAdmin)
