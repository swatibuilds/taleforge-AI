from pydantic import BaseModel
from typing import List


class Character(BaseModel):
    name: str
    description: str
    role: str


class ScenePlan(BaseModel):
    scene_number: int
    location: str
    summary: str
    key_events: List[str]
    mood: str


class StoryPlan(BaseModel):
    title: str
    genre: str
    language: str

    main_theme: str
    central_conflict: str

    main_characters: List[Character]

    story_structure: List[str]

    scenes: List[ScenePlan]

    ending: str