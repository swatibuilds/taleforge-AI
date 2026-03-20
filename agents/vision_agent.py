from graph.state import StoryState
from models.gemini_model import analyze_image
from prompts.vision_system_prompt import SYSTEM_PROMPT


def vision_agent(state: StoryState) -> StoryState:
    """
    Vision Agent

    Sends all images together to Gemini Vision and receives
    structured image-wise scene descriptions.
    """

    images = state["images"]

    prompt = f"""
{SYSTEM_PROMPT}

You will receive multiple images that form a sequence of scenes for a story.

Analyze EACH image carefully and produce a separate description section.

Important instructions:

1. Treat each image independently.
2. Clearly separate outputs using IMAGE NUMBER HEADINGS.
3. Follow the format below.

OUTPUT FORMAT:

IMAGE 1:
Scene Description:
...

Key Elements:
Environment:
Characters:
Objects:
Actions:
Mood:
Story Clues:

IMAGE 2:
Scene Description:
...

Key Elements:
Environment:
Characters:
Objects:
Actions:
Mood:
Story Clues:
"""

    # Send ALL images in one request
    response = analyze_image(images, prompt)

    # Split response into sections
    sections = response.split("IMAGE ")

    vision_descriptions = []

    for section in sections:
        if section.strip():
            vision_descriptions.append("IMAGE " + section.strip())

    # Update state
    state["vision_descriptions"] = vision_descriptions

    return state