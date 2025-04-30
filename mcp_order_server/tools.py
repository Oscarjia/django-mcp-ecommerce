import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from ui.models import Order, Inventory, Product

class OrderTools:
    """Collection of tools for order management."""
    
    @staticmethod
    def get_orders():
        """Get all product orders."""
        orders = Order.objects.all().prefetch_related('items')
        order_list = []
        
        for order in orders:
            order_items = []
            for item in order.items.all():
                order_items.append({
                    'guitarId': item.product.id,
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'name': item.product.name
                })
            
            order_list.append({
                'id': order.id,
                'customerName': order.customer_name,
                'orderDate': order.order_date.isoformat(),
                'totalAmount': float(order.total_amount),
                'items': order_items
            })
        
        return json.dumps(order_list, cls=DjangoJSONEncoder)
    
    @staticmethod
    def get_inventory():
        """Get product inventory."""
        inventory = Inventory.objects.all().select_related('product')
        inventory_list = []
        
        for item in inventory:
            inventory_list.append({
                'guitarId': item.product.id,
                'name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.product.price)
            })
        
        return json.dumps(inventory_list, cls=DjangoJSONEncoder)
    
    @staticmethod
    def purchase(items, customer_name):
        """Purchase products."""
        from django.db import transaction
        
        try:
            with transaction.atomic():
                # Calculate total amount
                total_amount = 0
                order_items = []
                
                for item in items:
                    guitar_id = item.get('guitarId')
                    quantity = item.get('quantity')
                    
                    # Get product and inventory
                    product = Product.objects.get(id=guitar_id)
                    inventory = Inventory.objects.get(product=product)
                    
                    # Check if enough inventory
                    if inventory.quantity < quantity:
                        return json.dumps({
                            'error': f'Not enough inventory for {product.name}. Available: {inventory.quantity}'
                        })
                    
                    # Update inventory
                    inventory.quantity -= quantity
                    inventory.save()
                    
                    # Calculate item total
                    item_total = product.price * quantity
                    total_amount += item_total
                    
                    order_items.append({
                        'product': product,
                        'quantity': quantity,
                        'price': product.price
                    })
                
                # Create order
                order = Order.objects.create(
                    customer_name=customer_name,
                    total_amount=total_amount
                )
                
                # Create order items
                for item_data in order_items:
                    from .models import OrderItem
                    OrderItem.objects.create(
                        order=order,
                        product=item_data['product'],
                        quantity=item_data['quantity'],
                        price=item_data['price']
                    )
                
                # Return order details
                return json.dumps({
                    'id': order.id,
                    'customerName': order.customer_name,
                    'orderDate': order.order_date.isoformat(),
                    'totalAmount': float(order.total_amount),
                    'items': [
                        {
                            'guitarId': item['product'].id,
                            'name': item['product'].name,
                            'quantity': item['quantity'],
                            'price': float(item['price'])
                        }
                        for item in order_items
                    ]
                }, cls=DjangoJSONEncoder)
                
        except Product.DoesNotExist:
            return json.dumps({'error': 'Product not found'})
        except Inventory.DoesNotExist:
            return json.dumps({'error': 'Inventory not found'})
        except Exception as e:
            return json.dumps({'error': str(e)})

# Define available tools with their descriptions and parameters
MCP_TOOLS = {
    "getOrders": {
        "description": "Get product orders",
        "parameters": {}
    },
    "getInventory": {
        "description": "Get product inventory",
        "parameters": {}
    },
    "purchase": {
        "description": "Purchase a product",
        "parameters": {
            "items": {
                "type": "array",
                "description": "List of guitars to purchase",
                "items": {
                    "type": "object",
                    "properties": {
                        "guitarId": {
                            "type": "integer",
                            "description": "ID of the guitar to purchase"
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity of guitars to purchase"
                        }
                    }
                }
            },
            "customerName": {
                "type": "string",
                "description": "Name of the customer"
            }
        }
    }
}