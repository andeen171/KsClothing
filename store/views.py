from rest_framework import viewsets, views
from rest_framework.response import Response
from .models import Product, Sale, Category
from .serializers import (
    ProductSerializer,
    SaleSerializer,
    CategorySerializer,
    StockReceivalSerializer,
)
from .paginations import PageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StockReceivalAPIView(views.APIView):
    def post(self, request, product_id, size_slug):
        obj = {
            "product": product_id,
            "stock": size_slug,
            "quantity": request.data["quantity"],
        }
        serializer = StockReceivalSerializer(data=obj)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        product = Product.objects.get(id=product_id)
        return Response(ProductSerializer(product).data)
