import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL

from langchain_ollama import ChatOllama


# -------------------------------
# Configure Gemini API
# -------------------------------

genai.configure(api_key=GEMINI_API_KEY)

# Native Gemini model (used only for vision)
model = genai.GenerativeModel(GEMINI_MODEL)


# -------------------------------
# Local LLM (Ollama)
# -------------------------------

def get_llm():
    """
    Returns a local Ollama LLM (Qwen2.5).
    Used by planner, generator, and critic agents.
    """

    llm = ChatOllama(
        model="qwen2.5:latest",   # change if using another variant
        temperature=0.7
    )

    return llm


# -------------------------------
# Gemini Text Generation (optional)
# -------------------------------

def generate_text(prompt: str) -> str:
    """
    Generate text using Gemini directly.
    (Not required if using Ollama everywhere)
    """

    response = model.generate_content(prompt)

    return response.text


# -------------------------------
# Gemini Vision Analysis
# -------------------------------
def analyze_image(images, prompt: str) -> str:
    """
    Analyze multiple images using Gemini Vision.
    """

    if not isinstance(images, list):
        images = [images]

    response = model.generate_content(
        [prompt] + images
    )

    return response.text