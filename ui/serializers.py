
from rest_framework import serializers
from ui.models import Product,OrderItem,Order,Inventory
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'order_date', 'total_amount', 'items']

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'quantity', 'last_updated']