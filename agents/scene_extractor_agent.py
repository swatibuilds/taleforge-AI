import json
from graph.state import StoryState
from models.gemini_model import get_llm
from prompts.scene_extractor_system_prompt import SYSTEM_PROMPT


def scene_extractor_agent(state: StoryState) -> StoryState:
    """
    Scene Extraction Agent

    Converts all vision descriptions into structured JSON scene data
    using a single LLM call.
    """

    llm = get_llm()

    vision_descriptions = state["vision_descriptions"]

    # Combine all descriptions
    descriptions_text = ""

    for i, desc in enumerate(vision_descriptions):
        descriptions_text += f"\n\nIMAGE {i+1} DESCRIPTION:\n{desc}"

    prompt = f"""
{SYSTEM_PROMPT}

You will receive descriptions for multiple images.

Convert EACH image description into a structured JSON object.

Return a JSON ARRAY where each element corresponds to one image.

Image Descriptions:
{descriptions_text}
"""

    response = llm.invoke(prompt)

    try:
        structured_scenes = json.loads(response.content.strip())

    except Exception:

        # fallback in case model output isn't perfect JSON
        structured_scenes = []

        for _ in vision_descriptions:
            structured_scenes.append({
                "location": None,
                "time_of_day": None,
                "environment_details": None,
                "characters": [],
                "objects": [],
                "actions": None,
                "mood": None,
                "story_clues": None
            })

    state["structured_scenes"] = structured_scenes

    return state