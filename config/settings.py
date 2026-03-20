import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Settings
GEMINI_MODEL = "gemini-2.5-flash"

# App Settings
MAX_IMAGES = 8
DEFAULT_STYLE = "Fantasy"
DEFAULT_LENGTH = "Medium"