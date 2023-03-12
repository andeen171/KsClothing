from django.urls import path, include
from .views import ProductViewSet, SaleViewSet, CategoryViewSet, StockReceivalAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("sales", SaleViewSet, basename="sale")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [
    path(r"", include(router.urls)),
    path(
        "product/<int:product_id>/stock/<slug:size_slug>/",
        StockReceivalAPIView.as_view(),
    ),
]
