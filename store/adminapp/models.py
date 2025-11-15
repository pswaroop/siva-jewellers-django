from django.db import models
from django.utils.text import slugify


class Banner(models.Model):
    """Model for storing banner images for the homepage or promotional sections"""
    name = models.CharField(max_length=200, help_text="Banner name for identification")
    image = models.ImageField(upload_to='banners/', help_text="Banner image")
    active = models.BooleanField(default=True, help_text="Whether this banner is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['active']),
        ]

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    """Model for product categories with auto-generated slugs"""
    category = models.CharField(max_length=200, unique=True, help_text="Category name")
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="URL-friendly version of category name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ['category']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category


class Product(models.Model):
    """Model for products with support for 2 images"""
    product_id = models.CharField(max_length=50, unique=True, help_text="Unique product identifier")
    product_name = models.CharField(max_length=300, help_text="Product name")
    category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.PROTECT, 
        related_name='products',
        help_text="Product category"
    )
    size = models.CharField(max_length=100, blank=True, null=True, help_text="Product size (e.g., S, M, L, XL)")
    image1 = models.ImageField(upload_to='products/', help_text="Primary product image")
    image2 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Secondary product image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['category', 'product_name']),
        ]

    def __str__(self):
        return f"{self.product_name} ({self.product_id})"


class Price(models.Model):
    """Model for storing gold and silver prices - standalone without relations"""
    gold_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Current gold price per unit"
    )
    silver_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Current silver price per unit"
    )
    effective_date = models.DateTimeField(auto_now_add=True, help_text="Date when these prices became effective")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"
        ordering = ['-effective_date']

    def __str__(self):
        return f"Gold: {self.gold_price} | Silver: {self.silver_price} (as of {self.effective_date.strftime('%Y-%m-%d')})"
