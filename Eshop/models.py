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
    # ✅ External image links (Mockaroo, CDN, etc.)
    image_url = models.URLField(blank=True, null=True)
    # ✅ Real uploaded files (stored in MEDIA_ROOT)
    image_file = models.ImageField(upload_to="products/", blank=True, null=True)
    new_arrival = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "2. Products"

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image_url = models.URLField(blank=True, null=True)
    image_file = models.ImageField(upload_to="products/gallery/", blank=True, null=True)

    primary = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "3. Product Images"
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(primary=True),
                name="unique_primary_image_per_product"
            )
        ]
        indexes = [
            models.Index(fields=["primary"], name="idx_primary_flag"),
        ]

    def __str__(self):
        if self.image_file:
            return f"{self.product.name} - {self.image_file.name}"
        elif self.image_url:
            return f"{self.product.name} - {self.image_url}"
        return f"{self.product.name} - No image"

    def save(self, *args, **kwargs):
        if self.primary:
            ProductImage.objects.filter(product=self.product, primary=True).exclude(pk=self.pk).update(primary=False)
        super().save(*args, **kwargs)

