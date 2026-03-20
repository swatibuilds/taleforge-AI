from graph.state import StoryState
from models.gemini_model import get_llm
from prompts.story_generator_system_prompt import SYSTEM_PROMPT


def story_generator_agent(state: StoryState) -> StoryState:
    """
    Story Generator Agent

    Generates the full narrative story using:
    - structured scenes extracted from images
    - the story plan produced by the planner agent
    - user preferences (genre, language, story length)
    """

    llm = get_llm()

    story_plan = state["story_outline"]
    structured_scenes = state["structured_scenes"]

    genre = state["genre"]
    language = state["language"]
    story_length = state["story_length"]

    prompt = f"""
{SYSTEM_PROMPT}

USER PREFERENCES
----------------
Genre: {genre}
Language: {language}
Story Length: {story_length}


STRUCTURED SCENE DATA
---------------------
These scenes were extracted from the uploaded images.

{structured_scenes}


STORY PLAN
----------
This is the high-level narrative structure produced by the planning agent.

{story_plan}


INSTRUCTIONS
------------

Write a complete story that:

• follows the story plan
• incorporates the scene details from the structured scene data
• maintains narrative consistency
• respects the selected genre
• is written in the requested language
• matches the requested story length

Ensure the story flows naturally from one scene to the next and remains engaging.
"""

    response = llm.invoke(prompt)

    story_text = response.content

    # store generated story
    state["generated_story"] = story_text

    return state