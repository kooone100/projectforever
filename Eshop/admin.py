from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from .models import Product, ProductImage, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ("image_preview",)
    fields = ("image_preview", "image_file", "image_url", "primary")

    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" style="max-height:100px;width:auto;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height:100px;width:auto;" />', obj.image_url)
        return "No image"
    image_preview.short_description = "Preview"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "primary":
            formfield.widget = admin.widgets.AdminRadioSelect(
                choices=[(True, "Primary"), (False, "Not Primary")]
            )
        return formfield


class HasPrimaryImageFilter(admin.SimpleListFilter):
    title = "Has Primary Image"
    parameter_name = "has_primary"

    def lookups(self, request, model_admin):
        return [("yes", "Yes"), ("no", "No")]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(images__primary=True).distinct()
        if self.value() == "no":
            return queryset.exclude(images__primary=True).distinct()
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "new_arrival", "primary_image_badge")
    list_filter = ("category", "new_arrival", HasPrimaryImageFilter)
    search_fields = ("name", "description")
    autocomplete_fields = ("category",)
    inlines = [ProductImageInline]

    def primary_image_badge(self, obj):
        primary = obj.images.filter(primary=True).first()
        if primary:
            if primary.image_file:
                return format_html(
                    '<span style="color:green;font-weight:bold;">★</span> '
                    '<img src="{}" style="max-height:80px;width:auto;" />',
                    primary.image_file.url
                )
            elif primary.image_url:
                return format_html(
                    '<span style="color:green;font-weight:bold;">★</span> '
                    '<img src="{}" style="max-height:80px;width:auto;" />',
                    primary.image_url
                )
        return "No primary image"
    primary_image_badge.short_description = "Primary Image"

    # ✅ Validation: enforce at least one primary image
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.images.filter(primary=True).exists():
            raise ValidationError(
                f"Product '{obj.name}' must have at least one primary image."
            )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image_preview", "primary")
    list_filter = ("primary",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" style="max-height:100px;width:auto;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height:100px;width:auto;" />', obj.image_url)
        return "No image"
    image_preview.short_description = "Image"
