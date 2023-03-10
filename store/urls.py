from django.urls import path, include
from .views import ProductViewSet, SaleViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('sales', SaleViewSet, basename='sale')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path(r'', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth')
]
