# In your terminal:
# python manage.py startapp ai_assistant

# ai_assistant/views.py
from django.http import JsonResponse
from django.shortcuts import render
import json
import uuid
from asgiref.sync import async_to_sync,sync_to_async

from .api import call_deepseek_api_func_calling,call_deepseek_api_mcp_way

def assistant_home(request):
    """View for rendering the AI assistant chat interface."""
    return render(request, 'chat_window.html')


async def generate_response(request):
    """API endpoint to generate AI responses."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")
            messages = data.get('messages', [])
            
            # Format messages for the API
            formatted_messages = []
            for message in messages:
                formatted_messages.append({
                    'role': message['role'],
                    'content': message['content']
                })
            # Add system message if not present
            if not any(msg['role'] == 'system' for msg in formatted_messages):
                formatted_messages.insert(0, {
                    'role': 'system',
                    'content': "You are a helpful assistant that provides information about my guitar e-commercial products."
                })
            

            print(f"Formatted messages: {formatted_messages}")
            # call the deepseek api use mcp way
            ai_assistant_response=await call_deepseek_api_mcp_way(formatted_messages)  
            # call the deepseek api use function calling way 
            # async_call_deepseek = sync_to_async(call_deepseek_api_func_calling)
            # ai_assistant_response = await async_call_deepseek(formatted_messages)
            
            response = {
                'id': str(uuid.uuid4()),
                'role': 'assistant',
                'content': f"{ai_assistant_response}",
                'parts': []
            }
            
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# Create a synchronous wrapper
sync_run_mcp = async_to_sync(generate_response)

def chat(request):
    """View for handling chat interactions."""
    if request.method == 'POST':
        return sync_run_mcp(request)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)