from django.contrib import admin
from .models import Advertise, HomeBanners










#------------------------------------------------------------------------------
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('Img', 'link')
admin.site.register(Advertise, AdvertiseAdmin)







#------------------------------------------------------------------------------
class HomeBannersAdmin(admin.ModelAdmin):
    list_display = ('BannerImg', 'title')
admin.site.register(HomeBanners, HomeBannersAdmin)








#End
