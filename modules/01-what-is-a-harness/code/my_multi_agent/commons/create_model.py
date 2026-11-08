"""
- File to house the model creation.
- the .env contains the API key, and is located inside the project root, 
   hence create the path accordingly.
"""

import os
import pathlib

from dotenv import load_dotenv

from google.adk.models import LiteLlm

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

def create_model():
    # TODO: try-except
    return LiteLlm(model='deepseek/deepseek-v4-flash', api_key=os.getenv('DEEPSEEK_API_KEY'))