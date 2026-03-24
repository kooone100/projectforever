from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "1. Categories"  # ✅ pluralized properly

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"  # ✅ added related_name for cleaner queries
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products")
    new_arrival = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "2. Products"

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"  # ✅ added related_name for cleaner queries
    )
    image = models.ImageField(upload_to="product_images")
    primary = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "3. Product Images"

    def __str__(self):
        return f"{self.product.name} - {self.image.name}"  # ✅ show file name instead of full path