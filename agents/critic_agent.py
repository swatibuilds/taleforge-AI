import json
from graph.state import StoryState
from models.gemini_model import get_llm
from prompts.critique_system_prompt import SYSTEM_PROMPT


def critic_agent(state: StoryState) -> StoryState:
    """
    Critic Agent

    Evaluates the generated story against the story plan
    and user preferences.
    """

    llm = get_llm()

    story_plan = state["story_outline"]
    story = state["generated_story"]

    genre = state["genre"]
    language = state["language"]
    length = state["story_length"]

    prompt = f"""
{SYSTEM_PROMPT}

User Preferences:
Genre: {genre}
Language: {language}
Story Length: {length}

Story Plan:
{story_plan}

Generated Story:
{story}
"""

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)

        state["critique_rating"] = result["rating"]
        state["critique_decision"] = result["decision"]
        state["critique_feedback"] = result["feedback"]

    except Exception:

        state["critique_rating"] = 5
        state["critique_decision"] = "REVISE"
        state["critique_feedback"] = "Critic agent failed to parse response."

    # if approved → set final story
    if state["critique_decision"] == "APPROVE":
        state["final_story"] = story

    return state