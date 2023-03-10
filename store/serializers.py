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
        fields = '__all__'


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class SaleSerializer(serializers.ModelSerializer):
    products = ReadWriteSerializerMethodField() 

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        sale_items_data = validated_data.pop('products')
        sale = Sale.objects.create(**validated_data)
        for sale_item in sale_items_data:
            sale_item['sale'] = sale.id
            serializer = SaleItemSerializer(data=sale_item)
            if serializer.is_valid():
                serializer.save()
        return sale

    def get_products(self, instance):
        qs = instance.items.all()
        serializer = SaleItemSerializer(qs, many=True)
        return serializer.data


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
