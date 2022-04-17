from django.urls import path
from .views import Products, ProductItem, Shops, ShopItem, Categories, CategoryItem, Attrs, AttrsItem, Search, ProductImg, ShopProducts, ShopProductsItem


urlpatterns = [
  path('shops', Shops.as_view(), name='shops'),
  path('shop/<int:id>', ShopItem.as_view(), name='shop_item'),
  path('products', Products.as_view(), name='products'),
  path('product/<int:id>', ProductItem.as_view(), name='product_item'),
  path('productimg', ProductImg.as_view(), name='product_img'),
  path('categories', Categories.as_view(), name='categories'),
  path('category/<int:id>', CategoryItem.as_view(), name='category_item'),
  path('attributes', Attrs.as_view(), name='attributes'),
  path('attribute/<int:id>', AttrsItem.as_view(), name='attribute_item'),
  path('search', Search.as_view(), name='search'),
  path('shop_products', ShopProducts.as_view(), name='shop_products'),
  path('shop_product/<int:id>', ShopProductsItem.as_view(), name='shop_product'),
]
