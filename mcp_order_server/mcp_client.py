import asyncio
import json
from mcp.client.stdio import stdio_client
from mcp import ClientSession,StdioServerParameters
import os
from openai import OpenAI
from dotenv import load_dotenv
# load_dotenv()
load_dotenv()

# path to the MCP server script
current_dir=os.path.dirname(os.path.abspath(__file__))
mcp_server_path=os.path.join(current_dir,"mcp_server.py")

serverparams=StdioServerParameters(command="python3",args=[mcp_server_path])

# Initialize the DeepSeek client with the API key
api_key=os.getenv("DEEPSEEK_API_KEY")
# Check if the API key is set
if api_key is None:
    raise ValueError("API key not found. Please set the DEEPSEEK_API_KEY environment variable.")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def llm_client(messages,tools=[]):
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
        
    response = client.chat.completions.create(
        **call_kwargs
            ) 
    return response.choices[0].message.content.strip()

def get_messages_to_identify_tool_argument(query,tools):
    """
    Get the messages to identify the tool argument.
    Args:
        query (str): The query to identify the tool argument.
    Returns:
        str: The prompt to identify the tool argument.
    """
    tools_description = "\n".join([f"- {tool.name}: {tool.description}"
     for tool in tools])
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that provides information about my guitar e-commercial products."
        },
        {
            "role": "user",
            "content": f"""Here are the tools available:\n{tools_description},\nPlease identify the tool and its arguments for the following query: {query}\n Remember You should only return a list of tools that should call to finish the query and the tool name and the arguments to be passed to the tool and in the format of:
            [
            {{
                "id": "tool_call_id",
                "tool": "tool-name",
                "arguments": {{"argument-name": "value"}}
            }},
            {{
                "id": "tool_call_id+1",
                "tool": "tool-name",
                "arguments": {{"argument-name": "value"}}
            }},
            {{
                "id": "tool_call_id+2",
                "tool": "tool-name",
                "arguments": {{"argument-name": "value"}}
            }},
            ]
            ]"""
        }
    ]
    
    return messages


async def run(messages):
    '''
    messages: list of messages. mostly the user query is the last message.
    message format:{role: "user", content: "query"}.
    '''
    try:
      async with stdio_client(serverparams) as (read,write):
            async  with ClientSession(read,write) as session:
                response=await session.initialize()
                #get the avaliable tools
                mcp_prompts=await session.list_prompts()
                print("Prompts available:")
                for prompt in mcp_prompts:
                    if prompt[0]=='prompts':
                        mcp_prompts=prompt[1]
                # print(f"mcp_prompts- {mcp_prompts}")    
                tools=await session.list_tools()
                for tool in tools:
                    if tool[0]=='tools':
                        tools=tool[1]
                # JSON Schema format compatible with OpenAI
                print(f"Tools available- {tools}\n")

                response = await session.call_tool(
                        name="get_api_products",
                        arguments={"messages": messages}
                )

                print(f"MCP Client Get Tool's response: {response.content[0].text}")
            
                return response.content[0].text
                
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

if __name__=="__main__":
    query="hi   there"
    asyncio.run(run(query))