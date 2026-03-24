from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")  # ✅ show key fields
    search_fields = ("name",)  # ✅ allow searching by name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "new_arrival")
    list_filter = ("category", "new_arrival")  # ✅ filter by category and new arrival
    search_fields = ("name", "description")  # ✅ allow searching
    autocomplete_fields = ("category",)  # ✅ better UX for large category lists


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "primary")
    list_filter = ("primary",)
    autocomplete_fields = ("product",)