from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from product.models import Category, Product, Comment
from product.serializers import CategorySerializer, ProductSerializer, CommentSerializer


# class Pagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 10000


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = Pagination


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


