from django.contrib import admin

from .models import ProductImage, Product, Category


class ProductImageInLine(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'timestamp')
    inlines = (ProductImageInLine,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
