from django.contrib import admin
from django.contrib.admin.models import LogEntry
from . import models
#from .models import Category, Shop, Product, ShopProducts, Attributes, ProductAttr, ProductImgs, ProductColor




'''





#------------------------------------------------------------------------------
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name','short_description', 'date_created','logo_tag')
    list_filter = ("category","date_created")
    search_fields = ['name',]
    raw_id_fields = ('category'),
admin.site.register(models.Shop, ShopAdmin)







#------------------------------------------------------------------------------
 #https://django-mptt.readthedocs.io/en/latest/admin.html#mptt-admin-draggablempttadmin
class CategoryMPTTModelAdmin(MPTTModelAdmin, TreeRelatedFieldListFilter):
    mptt_level_indent = 15   # specify pixel amount for this ModelAdmin only
    mptt_indent_field = "name"
    search_fields=['name__name']
admin.site.register(models.Category, DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title'),
    list_filter = ('parent',),
    raw_id_fields = ('parent',),
    search_fields=['name__name'],
    list_display_links=('indented_title',),)







#------------------------------------------------------------------------------
class AttributesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
admin.site.register(models.Attributes, AttributesAdmin)







#------------------------------------------------------------------------------
class ProductImgsInline(admin.TabularInline):
    model = ProductImgs
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('img_tag', 'name', 'category', 'date_created','approved')
    list_filter = ("category", "date_created", "approved")
    search_fields = ['name', 'code']
    raw_id_fields = ('category'),
    inlines = [ProductImgsInline]

admin.site.register(models.Product, ProductAdmin)












#------------------------------------------------------------------------------
class ProductAttrInline(admin.TabularInline):
    model = ProductAttr
    extra = 1

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1

class ShopProductsAdmin(admin.ModelAdmin):
    list_display = ('shop', 'qty', 'internal_code', 'product', 'available')
    list_filter = ("available", "shop")
    search_fields = ['shop__name', 'product__name', 'internal_code']
    raw_id_fields = ('shop','product')
    inlines = [ProductAttrInline, ProductColorInline]

admin.site.register(models.ShopProducts, ShopProductsAdmin)









'''







#End
