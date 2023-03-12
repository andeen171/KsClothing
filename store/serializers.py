from rest_framework import serializers
from .models import Product, Sale, Stock, Category, SaleItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("id", "size", "quantity")


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
        index = self.context.get("index", 0)
        try:
            stock = Stock.objects.filter(
                product=validated_data["product"], size=validated_data.pop("size")
            ).get()
            if validated_data["quantity"] > stock.quantity:
                raise serializers.ValidationError(
                    {
                        "products": {
                            f"{index}.quantity": ["Quantity is more than stock."]
                        }
                    }
                )
            stock.quantity -= validated_data["quantity"]
            stock.save()
        except Stock.DoesNotExist:
            raise serializers.ValidationError(
                {"products": {f"{index}.size": ["This size is not available."]}}
            )
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
        for i, sale_item in enumerate(sale_items_data):
            sale_item["sale"] = sale.id
            serializer = SaleItemSerializer(data=sale_item, context={"index": i})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return sale

    def get_products(self, instance):
        qs = instance.items.all()
        serializer = SaleItemSerializer(qs, many=True)
        return serializer.data


class StockReceivalSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    stock = serializers.CharField(max_length=1)
    quantity = serializers.IntegerField(min_value=1)

    def validate_stock(self, value):
        stock = Stock.objects.filter(product=self.initial_data["product"], size=value)
        if not stock.exists():
            raise serializers.ValidationError(
                {"stock": ["This size is not available."]}
            )
        return stock.get()

    def create(self, validated_data):
        stock = validated_data["stock"]
        stock.quantity += validated_data["quantity"]
        stock.save()
        return stock
