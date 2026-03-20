from typing import TypedDict, List, Dict, Optional
from PIL import Image


class StoryState(TypedDict):

    # ---------------------------
    # User Input
    # ---------------------------

    images: List[Image.Image]

    genre: str
    language: str
    story_length: str

    # ---------------------------
    # Vision Agent Output
    # ---------------------------

    vision_descriptions: List[str]

    # ---------------------------
    # Scene Extraction Agent
    # ---------------------------

    structured_scenes: List[Dict]

    # ---------------------------
    # Story Planning
    # ---------------------------

    story_outline: Dict

    # ---------------------------
    # Story Generation
    # ---------------------------

    generated_story: str

    # ---------------------------
    # Critic Agent
    # ---------------------------

    critique_feedback: Optional[str]

    critique_rating: Optional[int]

    critique_decision: Optional[str]

    # ---------------------------
    # Final Output
    # ---------------------------

    final_story: Optional[str]