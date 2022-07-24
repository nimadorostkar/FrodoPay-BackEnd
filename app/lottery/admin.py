from django.contrib import admin
from .models import Banner, UserScore, GetScore, Winner





#------------------------------------------------------------------------------
class BannerAdmin(admin.ModelAdmin):
    list_display = ('BannerImg','title')
admin.site.register(Banner, BannerAdmin)









#------------------------------------------------------------------------------
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score')
    list_filter = ('user',)
admin.site.register(UserScore, UserScoreAdmin)











#------------------------------------------------------------------------------
class GetScoreAdmin(admin.ModelAdmin):
    list_display = ('invite', 'deposit', 'register')
admin.site.register(GetScore, GetScoreAdmin)











#------------------------------------------------------------------------------
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('winners_qty', 'bonus_amount')
admin.site.register(Winner, WinnerAdmin)





#End
