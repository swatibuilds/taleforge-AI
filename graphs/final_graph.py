from langgraph.graph import StateGraph, END

from graph.state import StoryState

from agents.vision_agent import vision_agent
from agents.scene_extractor_agent import scene_extractor_agent
from agents.story_planner_agent   import story_planner_agent
from agents.story_generator_agent import story_generator_agent
from agents.critic_agent import critic_agent


def critic_router(state: StoryState):

    decision = state.get("critique_decision")

    if decision == "APPROVE":
        return "approved"

    return "revise"


def build_story_graph():

    workflow = StateGraph(StoryState)

    # -------------------------
    # Add Nodes (Agents)
    # -------------------------

    workflow.add_node("vision", vision_agent)
    workflow.add_node("scene_extraction", scene_extractor_agent)
    workflow.add_node("planner", story_planner_agent)
    workflow.add_node("generator", story_generator_agent)
    workflow.add_node("critic", critic_agent)

    # -------------------------
    # Set Entry Point
    # -------------------------

    workflow.set_entry_point("vision")

    # -------------------------
    # Normal Flow
    # -------------------------

    workflow.add_edge("vision", "scene_extraction")
    workflow.add_edge("scene_extraction", "planner")
    workflow.add_edge("planner", "generator")
    workflow.add_edge("generator", "critic")

    # -------------------------
    # Conditional Loop
    # -------------------------

    workflow.add_conditional_edges(
        "critic",
        critic_router,
        {
            "approved": END,
            "revise": "generator"
        }
    )

    # -------------------------
    # Compile Graph
    # -------------------------

    app = workflow.compile()

    return app