from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
        depth = 1

class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.SerializerMethodField()  # ✅ override image field

    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "primary"]

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()  # ✅ new field

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
            "primary_image",  # ✅ include in response
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(primary=True).first()  # ✅ use related_name="images"
        if primary and request:
            return request.build_absolute_uri(primary.image.url)
        return primary.image.url if primary else None

class NewArrivalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()          # ✅ override image field
    primary_image = serializers.SerializerMethodField()  # ✅ new field

    class Meta:
        model = Product
        fields = ["id", "name", "image", "price", "primary_image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(primary=True).first()  # ✅ uses related_name="images"
        if primary and request:
            return request.build_absolute_uri(primary.image.url)
        return primary.image.url if primary else None