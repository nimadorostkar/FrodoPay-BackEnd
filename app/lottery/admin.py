from django.contrib import admin
from .models import Banner, UserScore, GetScore





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









#End
