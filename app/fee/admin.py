from django.contrib import admin
from .models import Inventory, InputHistory





#------------------------------------------------------------------------------
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('amount',)
admin.site.register(Inventory, InventoryAdmin)








#------------------------------------------------------------------------------
class InputHistoryAdmin(admin.ModelAdmin):
    list_display = ('amount', 'transaction', 'created_at')
    list_filter = ('created_at',)
admin.site.register(InputHistory, InputHistoryAdmin)







#End
