from rest_framework import serializers
from .models import Banner, ProductCategory, Product, Price


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner model"""
    class Meta:
        model = Banner
        fields = ['id', 'name', 'image', 'active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializer for ProductCategory model"""
    class Meta:
        model = ProductCategory
        fields = ['id', 'category', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model with nested category details"""
    category_details = ProductCategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'product_id', 
            'product_name', 
            'category', 
            'category_details',
            'size', 
            'image1', 
            'image2', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_product_id(self, value):
        """Ensure product_id is unique"""
        if self.instance and self.instance.product_id == value:
            return value
        if Product.objects.filter(product_id=value).exists():
            raise serializers.ValidationError("A product with this product_id already exists.")
        return value


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for Price model"""
    class Meta:
        model = Price
        fields = ['id', 'gold_price', 'silver_price', 'effective_date', 'updated_at']
        read_only_fields = ['effective_date', 'updated_at']

    def validate(self, data):
        """Ensure prices are positive values"""
        if data.get('gold_price') and data['gold_price'] <= 0:
            raise serializers.ValidationError({"gold_price": "Gold price must be greater than zero."})
        if data.get('silver_price') and data['silver_price'] <= 0:
            raise serializers.ValidationError({"silver_price": "Silver price must be greater than zero."})
        return data
