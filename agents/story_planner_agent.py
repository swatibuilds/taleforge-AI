from graph.state import StoryState
from models.gemini_model import get_llm
from models.story_planner_schema import StoryPlan
from prompts.story_planner_system_prompt import SYSTEM_PROMPT

from langchain_core.output_parsers import PydanticOutputParser


def story_planner_agent(state: StoryState) -> StoryState:
    """
    Story Planner Agent

    Generates a structured story plan from scene data.
    """

    llm = get_llm()

    parser = PydanticOutputParser(pydantic_object=StoryPlan)

    format_instructions = parser.get_format_instructions()

    structured_scenes = state["structured_scenes"]

    genre = state["genre"]
    language = state["language"]
    story_length = state["story_length"]

    prompt = f"""
{SYSTEM_PROMPT}

User Preferences
----------------
Genre: {genre}
Language: {language}
Story Length: {story_length}

Structured Scene Data
---------------------
{structured_scenes}

{format_instructions}

IMPORTANT:
Return ONLY valid JSON.
Do not include explanations.
"""

    response = llm.invoke(prompt)

    try:

        story_plan = parser.parse(response.content)

    except Exception:

        # fallback minimal plan to avoid crashes
        story_plan = StoryPlan(
            title="Generated Story",
            genre=genre,
            language=language,
            main_theme="Adventure and discovery",
            central_conflict="The protagonist faces challenges during the journey",
            main_characters=[],
            story_structure=[
                "Introduction",
                "Rising Action",
                "Conflict",
                "Climax",
                "Resolution"
            ],
            scenes=[],
            ending="The journey ends with a meaningful discovery."
        )

    state["story_outline"] = story_plan

    return state