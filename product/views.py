from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


