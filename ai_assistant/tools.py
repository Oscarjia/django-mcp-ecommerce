import json
from django.core.serializers.json import DjangoJSONEncoder
from mcp.models import Product
import random

class Tools:
    '''
        Tools class to handle product data and serialization.
        This class provides methods to retrieve product data and serialize it to JSON format.   
        It also includes a method to get the list of all products.
    '''
    @staticmethod
    def get_products():
        '''
        Retrieve all product data.
        Returns:
            list: A list of dictionaries containing product data.
        '''
        try:
            products = Product.objects.all()
            product_list = []
            for product in products:
                product_list.append({
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': str(product.price),
                })
            return json.dumps(product_list, cls=DjangoJSONEncoder)
        except Product.DoesNotExist:
            return []
        except Exception as e:
            print(f"Error retrieving products: {e}")
            return []
        
    @staticmethod
    def get_product_by_id(product_id):
        '''
        Retrieve product data by ID.
        Args:
            product_id (int): The ID of the product to retrieve.
        Returns:
            dict: A dictionary containing product data, or None if not found.
        '''
        try:
            product = Product.objects.get(id=product_id)
            return {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
            }
        except Product.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error retrieving product with ID {product_id}: {e}")
            return None
    
    @staticmethod
    def recommend_products():
        '''
        Recommend products based on some criteria.
        This is a placeholder method and should be implemented with actual recommendation logic.
        Returns:
            list: A list of recommended product IDs.
        '''
        # Placeholder for recommendation logic
        id=random.randint(1, 5)
        try:
            product = Product.objects.get(id=id)
            return json.dumps({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
            })
        except Product.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error retrieving product with ID {id}: {e}")
            return None
        
# Define avaiilable tools with their descriptions and parameters
AvailableTools = {
        "get_products": {
            "description": "Get all products",
            "parameters": {}
        },
        "get_product_by_id": {
            "description": "Get product by ID",
            "parameters": {
                "product_id": {
                    "type": "integer",
                    "description": "The ID of the product to retrieve"
                }
            }
        },
        "recommend_products": {
            "description": "Recommend products",
            "parameters": {}
        }
    }
