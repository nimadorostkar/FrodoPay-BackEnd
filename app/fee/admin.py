from django.contrib import admin
from .models import Inventory, InputHistory, UserFeeRates, FeeRates





#------------------------------------------------------------------------------
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('amount',)
admin.site.register(Inventory, InventoryAdmin)








#------------------------------------------------------------------------------
class InputHistoryAdmin(admin.ModelAdmin):
    list_display = ('amount', 'transaction', 'created_at')
    list_filter = ('created_at',)
admin.site.register(InputHistory, InputHistoryAdmin)













#------------------------------------------------------------------------------
class FeeRatesAdmin(admin.ModelAdmin):
    list_display = ('withdrawal', 'deposit', 'transfer')
admin.site.register(FeeRates, FeeRatesAdmin)







#------------------------------------------------------------------------------
class UserFeeRatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'fee')
admin.site.register(UserFeeRates, UserFeeRatesAdmin)








#End
