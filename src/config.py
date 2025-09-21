import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        raise ValueError(
            "API key not found. Please set DEEPSEEK_API_KEY environment variable "
            "or create a .env file with your API key."
        )
    
    return {
        'api_key': api_key
    }
