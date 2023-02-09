from django.contrib import admin
from .models import Product, Sale, Category, Stock


class StockInline(admin.TabularInline):
    model = Stock
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'cost', 'category', 'created_at')
    list_filter = ('created_at', 'price', 'cost', 'category')
    search_fields = ('name',)

    def image_preview(self, obj):
        from django.utils.html import mark_safe
        return mark_safe(f'<img src="/storage/{obj.image}" width="150" height="150" />')

    image_preview.short_description = 'Preview'

    fieldsets = [
        ('Info', {'fields': ['name', 'description', 'category']}),
        ('File', {'fields': ['image', 'image_preview']}),
        ('Profit', {'fields': ['price', 'cost']}),
    ]
    readonly_fields = ('image_preview',)
    inlines = [StockInline]


class ProductInline(admin.TabularInline):
    model = Sale.products.through
    extra = 1


class SaleAdmin(admin.ModelAdmin):
    def products_list(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    products_list.short_description = 'Products'

    list_display = ('id', 'products_list', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('products__name',)
    inlines = [ProductInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Category)
