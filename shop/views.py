from django.shortcuts import render, get_object_or_404
from .serializers import ShopSerializer, ProductSerializer, CategorySerializer, ProductAttrSerializer, SearchSerializer, ProductImgsSerializer, ShopProductsSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import Shop, Product, Category , ProductAttr, ProductImgs, ShopProducts
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from . import serializers
from . import models
from django.db.models import Q





# ------------------------------------------------------- Attributes ------------

class Attrs(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductAttrSerializer
    queryset = ProductAttr.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['value','attribute']
    ordering_fields = ['id',]

    def get(self, request, format=None):
        queryset = ProductAttr.objects.all()
        query = self.filter_queryset(ProductAttr.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductAttrSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductAttrSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttrsItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ProductAttrSerializer

    def get(self, request, *args, **kwargs):
        attribute = get_object_or_404(ProductAttr, id=self.kwargs["id"])
        serializer = ProductAttrSerializer(attribute)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        attribute = get_object_or_404(ProductAttr, id=self.kwargs["id"])
        serializer = ProductAttrSerializer(attribute, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        attribute = get_object_or_404(ProductAttr, id=self.kwargs["id"])
        attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









# ------------------------------------------------------- Category ------------

class Categories(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent',]
    search_fields = ['name', 'parent']
    ordering_fields = ['id',]

    def get(self, request, format=None):
        queryset = Category.objects.all()
        query = self.filter_queryset(Category.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=self.kwargs["id"])
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=self.kwargs["id"])
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=self.kwargs["id"])
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










# ------------------------------------------------------- Shops ------------

class Shops(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'category', 'country', 'city']
    search_fields = ['name', 'phone','email','address', 'description']
    ordering_fields = ['id', 'date_created']

    def get(self, request, format=None):
        queryset = Shop.objects.all()
        query = self.filter_queryset(Shop.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ShopSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ShopSerializer

    def get(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












# ------------------------------------------------------- Products ------------

class Products(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'approved', 'brand']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['id', 'date_created']

    def get(self, request, format=None):
        queryset = Product.objects.all()
        query = self.filter_queryset(Product.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs["id"])
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs["id"])
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs["id"])
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









# ------------------------------------------------------- Search ------------

class Search(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response( 'please use POST method, and send query for search' , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = serializers.SearchSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response('There is a problem with the submitted information, please resend query',status=status.HTTP_400_BAD_REQUEST)
        search = data['q']
        if search:
            product = models.Product.objects.filter( Q(name__icontains=search) | Q(description__icontains=search) | Q(brand__icontains=search) | Q(code__icontains=search) )
            shop = models.Shop.objects.filter( Q(name__icontains=search) | Q(description__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search) | Q(address__icontains=search) )
            category = models.Category.objects.filter( Q(name__icontains=search) )

            product_serializer = ProductSerializer(product, many=True)
            shop_serializer = ShopSerializer(shop, many=True)
            category_serializer = CategorySerializer(category, many=True)

            search_data={ "product":product_serializer.data , "shops":shop_serializer.data, "categories":category_serializer.data }
            return Response(search_data, status=status.HTTP_200_OK)
        else:
            return Response('please send query for search', status=status.HTTP_400_BAD_REQUEST)














# ------------------------------------------------------- Attributes ------------

class ProductImg(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductImgsSerializer
    queryset = ProductImgs.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product',]
    search_fields = ['product',]
    ordering_fields = ['id',]

    def get(self, request, format=None):
        queryset = ProductImgs.objects.all()
        query = self.filter_queryset(ProductImgs.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductImgsSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductImgsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













# ------------------------------------------------------- Products ------------

class ShopProducts(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShopProductsSerializer
    queryset = ShopProducts.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'product', 'available']
    search_fields = ['shop__name', 'product__name', 'internal_code']
    ordering_fields = ['id']

    def get(self, request, format=None):
        queryset = models.ShopProducts.objects.all()
        query = self.filter_queryset(models.ShopProducts.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ShopProductsSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShopProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopProductsItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ShopProductsSerializer

    def get(self, request, *args, **kwargs):
        shop_product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        serializer = ShopProductsSerializer(shop_product)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        shop_product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        serializer = ShopProductsSerializer(shop_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        shop_product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        shop_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)













# End
