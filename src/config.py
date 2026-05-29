import os
from dotenv import load_dotenv

# 1. Load the environment variables
load_dotenv()

# 2. Define global constants from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "Your SERPER_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "Your PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "Your GEMINI_API_KEY")


# 3. Ensure critical keys exist before the app runs
if not all([SERPER_API_KEY, GEMINI_API_KEY, PINECONE_API_KEY]):
    raise ValueError("CRITICAL ERROR: Missing API keys in .env file")

PINECONE_INDEX_NAME = "openwebtext-archive"
