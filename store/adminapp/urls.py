from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BannerViewSet,
    ProductCategoryViewSet,
    ProductViewSet,
    PriceViewSet
)

# Create a router and register ViewSets
router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'categories', ProductCategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'prices', PriceViewSet, basename='price')

# Define app name for namespacing
app_name = 'adminapp'

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
