from rest_framework import serializers
from .models import Product, Sale, Stock, Category, SaleItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'value']


class SaleSerializer(serializers.ModelSerializer):
    products = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        sale_items_data = validated_data.pop('products')
        sale = Sale.objects.create(**validated_data)
        for sale_item in sale_items_data:
            SaleItem.objects.create(sale=sale, **sale_item)
        return sale


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
