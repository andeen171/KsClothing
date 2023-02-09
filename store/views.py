from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .paginations import PageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
