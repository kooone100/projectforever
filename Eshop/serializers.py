from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
        depth = 1

class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "primary"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image_file:
            url = obj.image_file.url
        elif obj.image_url:
            url = obj.image_url
        else:
            return None
        return request.build_absolute_uri(url) if request else url

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
            "image",
            "new_arrival",
            "images",
            "primary_image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image_file:
            url = obj.image_file.url
        elif obj.image_url:
            url = obj.image_url
        else:
            return None

        return request.build_absolute_uri(url) if request else url

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(primary=True).first()
        if not primary:
            return None

        if primary.image_file:
            url = primary.image_file.url
        elif primary.image_url:
            url = primary.image_url
        else:
            return None

        return request.build_absolute_uri(url) if request else url

class NewArrivalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image", "price", "primary_image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image_file:
            url = obj.image_file.url
        elif obj.image_url:
            url = obj.image_url
        else:
            return None

        return request.build_absolute_uri(url) if request else url

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(primary=True).first()
        if not primary:
            return None

        if primary.image_file:
            url = primary.image_file.url
        elif primary.image_url:
            url = primary.image_url
        else:
            return None

        return request.build_absolute_uri(url) if request else url