# agents/brand_guardian.py
from ollama import Client

# Minimal class definition needed for function signature (avoids circular import)
class AgentState: pass 

client = Client(host='http://localhost:11434')

def brand_guardian(state: AgentState) -> AgentState:
    """Checks content consistency, tone, and logo use against brand guidelines."""
    copy = state["copy"]
    strategy = state["strategy"]
    rev_count = state.get("revision_count", 0)
    
    # Mocking the LLM behavior to force a rejection and then a pass for the demo flow
    if rev_count == 0:
        # Initial copy is mocked to be generic
        feedback = "REJECT: Copy tone mismatch. The copy is too formal and generic, failing the 'Playful Tone Score'. Target: copywriter"
        state["rejection_target"] = "copywriter"
    else:
        # After copywriter runs the revision
        feedback = "PASS: Tone is now acceptable. Visual consistency check passed after revision."
        state["rejection_target"] = ""
        
    state["brand_feedback"] = feedback
    print(f"Brand Guardian Feedback (Rev {rev_count}): {feedback[:40]}...")
    return state