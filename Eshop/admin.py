from django.utils.html import format_html
from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")  # ✅ show key fields
    search_fields = ("name",)  # ✅ allow searching by name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "new_arrival", "image_tag")
    list_filter = ("category", "new_arrival")
    search_fields = ("name", "description")
    autocomplete_fields = ("category",)

    def image_tag(self, obj):
        if obj.image:
            # ✅ Correct: pass the URL as an argument
            return format_html('<img src="{}" style="height:50px;width:auto;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Image"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "primary")
    list_filter = ("primary",)
    autocomplete_fields = ("product",)