from django.contrib import admin
from .models import Top, Features, Description, Banners, MobileBanners, Footer, Socials




#------------------------------------------------------------------------------
class TopAdmin(admin.ModelAdmin):
    list_display = ('slogan_text', 'buttonText_text')
admin.site.register(Top, TopAdmin)




#------------------------------------------------------------------------------
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
admin.site.register(Features, FeaturesAdmin)





#------------------------------------------------------------------------------
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
admin.site.register(Description, DescriptionAdmin)





#------------------------------------------------------------------------------
class BannersAdmin(admin.ModelAdmin):
    list_display = ('link',)
admin.site.register(Banners, BannersAdmin)





#------------------------------------------------------------------------------
class MobileBannersAdmin(admin.ModelAdmin):
    list_display = ('link',)
admin.site.register(MobileBanners, MobileBannersAdmin)






#------------------------------------------------------------------------------
class SocialsInline(admin.TabularInline):
    model = Socials
    extra = 1
#------------------------------------------------------------------------------
class FooterAdmin(admin.ModelAdmin):
    list_display = ('slogan_text', 'copyright_text')
    inlines = [SocialsInline]
admin.site.register(Footer, FooterAdmin)












#End
