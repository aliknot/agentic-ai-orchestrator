import os
from dotenv import load_dotenv

# 1. Load the environment variables
load_dotenv()

# 2. Define global constants from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# 3. Ensure critical keys exist before the app runs
if not GROQ_API_KEY:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY is missing from .env")
if not SERPER_API_KEY:
    raise ValueError("CRITICAL ERROR: SERPER_API_KEY is missing from .env")
