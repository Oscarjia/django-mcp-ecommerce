import json
import mcp
from mcp.server.fastmcp import FastMCP,Context
from django.core.serializers.json import DjangoJSONEncoder
import httpx
import os
from openai import OpenAI
from dotenv import load_dotenv
# load_dotenv()
load_dotenv()
# Initialize the DeepSeek client with the API key
api_key=os.getenv("DEEPSEEK_API_KEY")
# Check if the API key is set
if api_key is None:
    raise ValueError("API key not found. Please set the DEEPSEEK_API_KEY environment variable.")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
# Instantiate the FastMCP server
mcp = FastMCP(name = "Django-MCP-Ecommerce_Server", description="MCP server for Django E-commerce application")

@mcp.prompt()
def adam():
    """
    Adam is a virtual assistant that helps you with your shopping needs.
    You can ask her about products, orders, and inventory.
    """
    return "Hello! I'm Adam, your virtual shopping assistant in 千问LLM . How can I help you today?"

@mcp.resource("boss-memo://get_boss_memo")
def get_boss_memo():

    """
    Get the boss's memo.
    Returns:
        str: The boss's memo.
    """
    with open('./memo/boss_memo.md', 'r') as file:
        memo = file.read()
    return memo

@mcp.tool(name="call_llm_client", description="call LLM for chat completion")
def call_llm_client(messages=list):
    """
    call LLM for chat completion,the messages should be in the format of a list of dictionaries
    Args:
        messages (list): The messages to send to the LLM. For example:
            [
                {"role": "user", "content": "Hello!"},  
                {"role": "assistant", "content": "Hi! How can I help you?"}
            ]
        tools (list): The tools to use for the LLM. For example:
            [
                {
                "type": "function",
                "function":{
                    "name": tool_name,
                    "description": tool_info_description"],
                    "parameters": {
                        "type": "object",
                        "properties": {
                            param_name: {
                                "type": param_info["type"],
                                "description": param_info["description"]
                            } for param_name, param_info in tool_info.get("parameters", {}).items()
                        }
                    }
                }
               }
            ]
    Returns:
        str: The response from the LLM.  if the response is a function call, it will be in the format of:
            {
                "tool": "tool-name",
                "arguments": {
                    "argument-name": "value"
                }
            }
    """
    try:
        call_kwargs = {
            "model":        "deepseek-chat",
            "messages":     messages,
            "tool_choice":  "auto",
            "max_tokens":   1024,
            "temperature":  0.7,
            "stream":       False,
        }
        # 

        tools=[{'type': 'function', 'function': {'name': 'call_llm_client', 'description': 'call LLM for chat completion', 'parameters': {'type': 'object', 'properties': {'messages': {'title': 'messages', 'type': 'string'}, 'tools': {'title': 'tools', 'type': 'string'}}, 'required': []}}}, {'type': 'function', 'function': {'name': 'get_api_products', 'description': 'Get all products', 'parameters': {'type': 'object', 'properties': {'messages': {'title': 'Messages', 'type': 'array'}}, 'required': ['messages']}}}]
        # Only include tools if the list isn’t empty or it will throw an error
        if tools:
                call_kwargs["tools"] = tools

        print(f"MCP Server Calling LLM with arguments: {call_kwargs}")
            
        response = client.chat.completions.create(
            **call_kwargs
                ) 
    except Exception as e:
            print(f"Error calling LLM: {e}")
            return {"error": "Failed to call LLM"}

    return response.choices[0].message.content.strip()

#get products
@mcp.tool(name="get_api_products", description="Get all products")
async def get_api_products(context: Context,messages:list[dict]):
    """
    Get all guitar products.
    Returns:
        list: A list of all guitar products.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/ui/api/products/')
        if response.status_code == 200:
            products = response.json()
            # only return the description and price of each product
            products = [
                {
            
                    'name': product['name'],
                    'description': product['description'],
                    'price': product['price'],
                }
                for product in products
            ]
            # call_llm_client
            messages.append({
                "role": "assistant",
                "content": f"Here are the products: {products}"
            })
            response=call_llm_client(messages)
            return response
        else:
            return {'error': 'Failed to fetch products'}
        
if __name__=="__main__":
    # Run the server
    mcp.run(transport='stdio')
        
# # get orders
# @mcp.tool(name="getOrders", description="Get all product orders")
# async def get_orders(context: Context):
#     """
#     Get all product orders.
#     Returns:
#         list: A list of all orders.
#     """
#     async with httpx.AsyncClient() as client:
#         response = await client.get('http://localhost:8000/api/orders/')
#         if response.status_code == 200:
#             orders = response.json()
#             return orders
#         else:
#             return {'error': 'Failed to fetch orders'}
# # get inventory
# @mcp.tool(name="getInventory",description="Get all product inventory",vesrion="1.0.0")
# async def get_inventory(context: Context):
#     """
#     Get all product inventory.
#     Returns:
#         list: A list of all products in the inventory.
#     """
#     async with httpx.AsyncClient() as client:
#         response = await client.get('http://localhost:8000/api/inventory/')
#         if response.status_code == 200:
#             inventory = response.json()
#             return inventory
#         else:
#             return {'error': 'Failed to fetch inventory'}
# # purchase
# @mcp.tool(name="purchase",description="Purchase products",version="1.0.0")
# async def purchase(items:list[dict],customerName:str,context:Context):
#     async with httpx.AsyncClient() as client:
#         response = await client.post('http://localhost:8000/api/purchase/', json={
#             'items': items,
#             'customerName': customerName
#         })
#         if response.status_code == 200:
#             result = response.json()
#             return result
#         else:
#             return {'error': 'Failed to process purchase'}
