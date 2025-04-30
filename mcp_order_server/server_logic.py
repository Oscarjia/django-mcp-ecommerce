import json
import mcp
from mcp.server.fastmcp import FastMCP,Context
from django.core.serializers.json import DjangoJSONEncoder
import httpx
# Instantiate the FastMCP server
server = FastMCP(name = "Django-MCP-Ecommerce", version="1.0.0", description="MCP server for Django E-commerce application")

# get orders
@mcp.tool(name="getOrders", description="Get all product orders")
async def get_orders(context: Context):
    """
    Get all product orders.
    Returns:
        list: A list of all orders.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/api/orders/')
        if response.status_code == 200:
            orders = response.json()
            return orders
        else:
            return {'error': 'Failed to fetch orders'}
# get inventory
@mcp.tool(name="getInventory",description="Get all product inventory",vesrion="1.0.0")
async def get_inventory(context: Context):
    """
    Get all product inventory.
    Returns:
        list: A list of all products in the inventory.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/api/inventory/')
        if response.status_code == 200:
            inventory = response.json()
            return inventory
        else:
            return {'error': 'Failed to fetch inventory'}
# purchase
@mcp.tool(name="purchase",description="Purchase products",version="1.0.0")
async def purchase(items:list[dict],customerName:str,context:Context):
    async with httpx.AsyncClient() as client:
        response = await client.post('http://localhost:8000/api/purchase/', json={
            'items': items,
            'customerName': customerName
        })
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return {'error': 'Failed to process purchase'}
