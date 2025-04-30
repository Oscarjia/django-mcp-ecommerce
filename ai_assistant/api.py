from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from .tools import AvailableTools,Tools
# Load environment variables from .env file
load_dotenv()
# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
api_key=os.getenv("DEEPSEEK_API_KEY")
# Check if the API key is set
if api_key is None:
    raise ValueError("API key not found. Please set the DEEPSEEK_API_KEY environment variable.")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def call_deepseek_api(messages):
    """
    Call the DeepSeek API to get a response from the AI model.
    Supports function calling to interact with the tools defined in AvailableTools.
    """
    tools=[]
    print(f"Types of Tools: {type(AvailableTools)}")
    for tool_name, tool_info in AvailableTools.items():
            # Add the tool to the tools list
            print(f"Tool name: {tool_name}")
            print(f"Tool tool_info: {tool_info}")
            tools.append({
                "type": "function",
                "function":{
                    "name": tool_name,
                    "description": tool_info["description"],
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
            })
    print(f"Tools: {tools}")
    # Add the tools to the API call
    # Base args for the call
    call_kwargs = {
        "model":        "deepseek-chat",
        "messages":     messages,
        "tool_choice":  "auto",
        "max_tokens":   1024,
        "temperature":  0.7,
        "stream":       False,
    }
    # Only include tools if the list isn’t empty or it will throw an error
    if tools:
        call_kwargs["tools"] = tools
    # Make the API call
    response = client.chat.completions.create(
        **call_kwargs
    )
    # Process the response
    choice = response.choices[0]
    assistant_message = choice.message
   
    print(f"LLM Response message: {assistant_message}")
    # Check if the response contains tool calls 
    if hasattr(assistant_message, "tool_calls") and assistant_message.tool_calls:
        # If there are tool calls, we need to process them
        messages.append({
            "role": "assistant",
            "tool_calls": assistant_message.tool_calls
        })
        # Iterate through the tool calls
        # and call the appropriate tool function
        # Append the assistant's response to the tool call
        # Example tool call
        # ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0_c8c96c4a-f678-48ab-9425-5b6761aedeb7', function=Function(arguments='{}', name='recommend_products'), type='function', index=0)])
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            # 1) Get the raw JSON string
            tool_args = tool_call.function.arguments or "{}"
            print(f"Tool name and args: {tool_name}, {tool_args}")
            # 2) Convert it to a dict
            try:
                    tool_args = json.loads(tool_args)
            except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON arguments: {tool_args}")
            # Call the appropriate tool function
            if tool_name in AvailableTools:
                tool_function = getattr(Tools, tool_name, None)
                if tool_function:
                    tool_response = tool_function(**tool_args)
                    print(f"Tool response: {tool_response}")
                    # Append the tool response to the assistant's message
                    # Update the tool call with the tool response
                    messages.append(
                        {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_name,
                        "content": tool_response
                        }
                    ) 
        print(f"Messages after tool call: {messages}") 
        #Make a new API call with the tool response
        second_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1024,
            temperature=0.7,
            stream=False
        ) 
        # Process the second response
        print(f"Second LLM Response message: {second_response}")
        return second_response.choices[0].message.content
    # If no tool calls, return the assistant's response
    return assistant_message.content
