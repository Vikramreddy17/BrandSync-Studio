# graph.py (LangGraph Workflow - FINAL WORKING VERSION)

from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
import sys

# Add the agents directory to the system path for successful import
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# --- 1. State Definition (SINGLE SOURCE OF TRUTH) ---
class AgentState(TypedDict):
    """
    Represents the state of our graph, defining all data passed between agents.
    """
    brief: str
    strategy: str              # Strategist's output: tone, keywords, goals
    copy: str                  # Copywriter's output: caption/text
    image_prompt: str          # Designer's input: text-to-image prompt
    image_path: str            # Designer's output: path to generated image
    brand_feedback: str        # Brand Guardian's critique (or "PASS")
    compliance_report: str     # Compliance Officer's report (or "PASS")
    final_output: dict         # Final structure {copy, image_path, report}
    revision_count: int        # Counter for validation loop
    rejection_target: str      # Where to send the revision ("copywriter" or "designer")

# --- 2. Import Agent Functions ---
# Import functions using the explicit module path from the 'agents' directory
from agents.strategist import strategist
from agents.copywriter import copywriter
from agents.designer import designer
from agents.brand_guardian import brand_guardian
from agents.compliance import compliance_officer

# --- 3. Conditional Edge Routing ---

def route_to_revision(state: AgentState) -> str:
    """Decides if we need a revision, and where to route it, or if the content is ready."""
    print(f"--- Brand Guardian Result: {state['brand_feedback'][:40]}... ---")
    
    if state["revision_count"] >= 2:
        print("--- Max Revisions Reached. FORCING END. ---")
        return END

    if "REJECT" in state["brand_feedback"]:
        target = state.get("rejection_target", "copywriter")
        print(f"--- Revision needed. Routing to: {target} ---")
        return target
    
    print("--- Brand PASS. Routing to Compliance. ---")
    return "compliance"

# --- 4. Build Graph ---
def build_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("strategist", strategist)
    workflow.add_node("copywriter", copywriter)
    workflow.add_node("designer", designer)
    workflow.add_node("brand_guardian", brand_guardian)
    workflow.add_node("compliance", compliance_officer)

    workflow.set_entry_point("strategist")

    workflow.add_edge("strategist", "copywriter")
    workflow.add_edge("copywriter", "designer")
    workflow.add_edge("designer", "brand_guardian")
    
    workflow.add_conditional_edges(
        "brand_guardian",
        route_to_revision,
        {
            "copywriter": "copywriter",
            "designer": "designer",
            "compliance": "compliance"
        }
    )
    workflow.add_edge("compliance", END)

    return workflow.compile()

# Example execution (Run with: python graph.py)
if __name__ == "__main__":
    app = build_workflow()
    os.makedirs("output_content", exist_ok=True)
    
    initial_state = {"brief": "Create an engaging social media post for our new autonomous AI agency launch.", "revision_count": 0}
    
    print("\n\n--- Starting BrandSync Studio Workflow ---")
    
    final_state = {}
    for s in app.stream(initial_state):
        print(s)
        final_state.update(s)
    
    print("\n\n==========================================")
    print("🚀 FINAL OUTPUT GENERATED 🚀")
    print("==========================================")
    if 'final_output' in final_state:
        print(f"Copy: {final_state['final_output']['copy']}")
        print(f"Image Path: {final_state['final_output']['image_path']}")
        print(f"Compliance Report: {final_state['final_output']['report']}")
    else:
         print("Workflow ended before final output. Check revision count.")
    print(f"Total Cycles: {final_state.get('revision_count', 0)}")