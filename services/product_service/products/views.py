from rest_framework import status
from django.core.cache import cache
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .serializers import (
    CategorySerializer,
    ProductSerializer
)
from .models import Category, Product, GaleryProducts


class CategoryViewSet(ViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    cache_key = "category_list"

    def list(self, request):
        cache_data = cache.get(self.cache_key)
        if cache_data is not None:
            return Response(cache_data)
        
        categors = self.queryset
        serializer_data = self.serializer_class(instance=categors, many=True)
        cache.set(self.cache_key, serializer_data.data)
        return Response(data=serializer_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            cache.delete(self.cache_key)
            return Response(data=serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            category = self.queryset.get(id=pk)
            serializer_data = self.serializer_class(instance=category)
            return Response(data=serializer_data.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message":"This category does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        category = self.queryset.get(id=pk)
        serializer_data = self.serializer_class(data=request.data, instance=category, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            cache.delete(self.cache_key)
            return Response(data=serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            category = self.queryset.get(id=pk)
            category.delete()
            cache.delete(self.cache_key)
            return Response({"message":"Category Deleted"}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message":"This category does not exist."}, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(ViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    cache_key = "product_list"

    def list(self, request):
        cache_data = cache.get(self.cache_key)
        if cache_data is not None:
            return Response(cache_data, status=status.HTTP_200_OK)

        products = self.queryset
        serializer_data = self.serializer_class(instance=products, many=True)
        cache.set(self.cache_key, serializer_data.data)
        return Response(data=serializer_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            cache.delete(self.cache_key)
            return Response(data=serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            product = self.queryset.get(id=pk)
            serializer_data = self.serializer_class(instance=product)
            return Response(data=serializer_data.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"message":"This product does not exist."})


    def update(self, request, pk=None):
        product = self.queryset.get(id=pk)
        serializer_data = self.serializer_class(data=request.data, instance=product, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            cache.delete(self.cache_key)
            return Response(data=serializer_data.data, status=status.HTTP_200_OK)
        return Response(data=serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            product = self.queryset.get(id=pk)
            product.delete()
            cache.delete(self.cache_key)
            return Response({"message":"Product Deleted"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"message":"This product does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
