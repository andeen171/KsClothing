from rest_framework import serializers
from .models import Product, Sale, Stock, Category, SaleItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'size', 'quantity') 


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    stocks = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

    def get_stocks(self, obj):
        stocks = obj.stock_set.all()
        return StockSerializer(stocks, many=True).data


class SaleItemSerializer(serializers.ModelSerializer):
    size = serializers.CharField(write_only=True)

    class Meta:
        model = SaleItem
        fields = "__all__"

    def create(self, validated_data):
        validated_data.pop("size")
        sale_item = SaleItem.objects.create(**validated_data)
        return sale_item


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class SaleSerializer(serializers.ModelSerializer):
    products = ReadWriteSerializerMethodField()

    class Meta:
        model = Sale
        fields = "__all__"

    def create(self, validated_data):
        sale_items_data = validated_data.pop("products")
        sale = Sale.objects.create(**validated_data)
        for sale_item in sale_items_data:
            sale_item["sale"] = sale.id
            serializer = SaleItemSerializer(data=sale_item)
            if serializer.is_valid():
                serializer.save()
                stock = Stock.objects.filter(
                    product=sale_item["product"], size__icontains=sale_item["size"]
                ).get()
                stock.quantity -= sale_item["quantity"]
                stock.save()
        return sale

    def get_products(self, instance):
        qs = instance.items.all()
        serializer = SaleItemSerializer(qs, many=True)
        return serializer.data
