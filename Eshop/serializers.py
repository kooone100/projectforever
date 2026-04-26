from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "primary"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "image",          # main product image
            "new_arrival",
            "images",         # gallery images
            "primary_image",  # computed primary gallery image
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(primary=True).first()
        if primary and primary.image:
            url = primary.image.url
            return request.build_absolute_uri(url) if request else url
        return None


class NewArrivalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image", "price", "primary_image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(primary=True).first()
        if primary and primary.image:
            url = primary.image.url
            return request.build_absolute_uri(url) if request else url
        return None
