from openai import OpenAI
from dotenv import load_dotenv
import os
# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
api_key=os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def call_deepseek_api(user_input):
    """
    Call the DeepSeek API to get a response from the AI model.
    """
    # Example of calling the DeepSeek API
    # Replace with your actual API call and parameters
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant,can ansower questions for the ecommerce website."},
            {"role": "user", "content": user_input},
    ],
        max_tokens=1024,
        temperature=0.7,
        stream=False
    )
    return response.choices[0].message.content
