from itertools import product

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, NewArrivalSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryView(APIView):
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductListView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        try:
            search_query = request.GET.get('search', '')
            products = Product.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(result_page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data['total_count'] = products.count()
            return response
        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductByCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, category_id):
        try:
            category = get_object_or_404(Category, id=category_id)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductImageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            images = ProductImage.objects.filter(product=product)
            serializer = ProductImageSerializer(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewArrivalView(APIView):
    def get(self, request):
        new_arrivals = Product.objects.filter(new_arrival=True)
        serializer = NewArrivalSerializer(new_arrivals, many=True)
        return Response(serializer.data)

class FaucetView(APIView):
    def get(self, request):
        faucets = Product.objects.filter(category__name='Faucets')
        serializer = ProductSerializer(faucets, many=True)
        data = serializer.data
        for faucet in data:
            faucet['image'] = settings.BASE_URL + faucet['image']
        return Response(data)

class SanwareView(APIView):
    def get(self, request):
        sanware = Product.objects.filter(category__name='Sanitary Ware')
        serializer = ProductSerializer(sanware, many=True)
        data = serializer.data
        for sanware in data:
            sanware['image'] = settings.BASE_URL + sanware['image']
        return Response(data)