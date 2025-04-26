from rest_framework import serializers
from ui.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image_url', 'created_at', 'updated_at'] 