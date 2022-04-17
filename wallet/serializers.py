from rest_framework import serializers
#from .models import Shop, Product, Category, Attributes, ProductAttr, ProductImgs, ShopProducts


'''


#------------------------------------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')






#------------------------------------------------------------------------------
class ProductAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttr
        fields = ('id', 'product', 'product_name', 'attribute', 'attribute_name', 'value')






#------------------------------------------------------------------------------
class ProductImgsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImgs
        fields = ('id', 'product', 'product_name', 'img')







#------------------------------------------------------------------------------
class ShopSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    class Meta:
        model = Shop
        fields = ('id' ,'name', 'user','user_mobile', 'phone', 'email', 'country', 'city', 'address', 'postal_code', 'lat_long', 'description','category', 'logo', 'cover', 'shaba_number', 'card_number', 'bank_account_number', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'date_created')







#------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    #attributes = AttributesSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'irancode', 'approved', 'banner', 'brand', 'link', 'category', 'category_name', 'description', 'datasheet', 'date_created')






class SearchSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=64, allow_null=False)












#------------------------------------------------------------------------------
class ShopProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProducts
        fields = ('id' ,'available', 'shop','product', 'internal_code', 'qty', 'retail_price', 'medium_volume_price', 'min_medium_num', 'wholesale_price', 'min_wholesale_num')


'''









#End
