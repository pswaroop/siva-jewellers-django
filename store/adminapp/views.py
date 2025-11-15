from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Banner, ProductCategory, Product, Price
from .serializers import (
    BannerSerializer, 
    ProductCategorySerializer, 
    ProductSerializer, 
    PriceSerializer
)


class BannerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Banner model
    Provides CRUD operations for banners
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active']
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def active_banners(self, request):
        """Get only active banners"""
        active = Banner.objects.filter(active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ProductCategory model
    Provides CRUD operations for product categories
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['category', 'slug']


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model
    Provides CRUD operations for products
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'size']
    search_fields = ['product_name', 'product_id']
    ordering_fields = ['created_at', 'product_name']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_slug>[-\\w]+)')
    def by_category(self, request, category_slug=None):
        """Get products by category slug"""
        products = self.queryset.filter(category__slug=category_slug)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def latest_featured(self, request):
        latest_products = Product.objects.all().order_by('-created_at')[:6]  # top 6
        serializer = self.get_serializer(latest_products, many=True)
        return Response(serializer.data)


class PriceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Price model
    Provides CRUD operations for gold and silver prices
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    ordering = ['-effective_date']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest price"""
        latest_price = Price.objects.first()
        if latest_price:
            serializer = self.get_serializer(latest_price)
            return Response(serializer.data)
        return Response({'message': 'No prices available'}, status=404)
