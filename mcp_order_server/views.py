from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.http import JsonResponse
from ui.models import Product
from ui.models import Order, Inventory, OrderItem
from ui.serializers import OrderSerializer, InventorySerializer
from .tools import OrderTools
import json


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

@api_view(['GET'])
def get_orders(request):
    """API endpoint to get all orders."""
    orders_json = OrderTools.get_orders()
    return JsonResponse(json.loads(orders_json), safe=False)

@api_view(['GET'])
def get_inventory(request):
    """API endpoint to get inventory."""
    inventory_json = OrderTools.get_inventory()
    return JsonResponse(json.loads(inventory_json), safe=False)

@api_view(['POST'])
def purchase(request):
    """API endpoint to purchase products."""
    try:
        data = request.data
        items = data.get('items', [])
        customer_name = data.get('customerName', '')
        
        if not items or not customer_name:
            return JsonResponse({'error': 'Items and customerName are required'}, status=400)
        
        result_json = OrderTools.purchase(items, customer_name)
        result = json.loads(result_json)
        
        if 'error' in result:
            return JsonResponse(result, status=400)
        
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# MCP Server implementation
@api_view(['POST'])
def mcp_tool_handler(request, tool_name):
    """Handle MCP tool requests."""
    try:
        data = request.data
        
        if tool_name == 'getOrders':
            orders_json = OrderTools.get_orders()
            return JsonResponse({
                'content': [{'type': 'text', 'text': orders_json}]
            })
        
        elif tool_name == 'getInventory':
            inventory_json = OrderTools.get_inventory()
            return JsonResponse({
                'content': [{'type': 'text', 'text': inventory_json}]
            })
        
        elif tool_name == 'purchase':
            items = data.get('items', [])
            customer_name = data.get('customerName', '')
            
            if not items or not customer_name:
                return JsonResponse({'error': 'Items and customerName are required'}, status=400)
            
            result_json = OrderTools.purchase(items, customer_name)
            return JsonResponse({
                'content': [{'type': 'text', 'text': result_json}]
            })
        
        else:
            return JsonResponse({'error': f'Unknown tool: {tool_name}'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def mcp_tools(request):
    """Return available MCP tools."""
    from .tools import MCP_TOOLS
    
    tools_list = []
    for name, info in MCP_TOOLS.items():
        tools_list.append({
            'name': name,
            'description': info['description'],
            'parameters': info['parameters']
        })
    
    return JsonResponse({
        'name': 'Django MCP Server',
        'version': '1.0.0',
        'tools': tools_list
    })
