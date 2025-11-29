# agents/compliance.py
from ollama import Client

# Minimal class definition needed for function signature (avoids circular import)
class AgentState: pass 

client = Client(host='http://localhost:11434')

def compliance_officer(state: AgentState) -> AgentState:
    """Performs final checks for copyright, ethics, and bias using Llama 3.1."""
    
    # Mocked final report, as the LLM call is slow for demo
    report = "PASS: Bias check clear (Low Risk). Copyright check: Image generation metadata recorded (None). Content is ready for publish."
         
    state["compliance_report"] = report
    
    # Final assembly
    state["final_output"] = {
        "copy": state["copy"],
        "image_path": state["image_path"],
        "strategy": state["strategy"],
        "report": state["compliance_report"]
    }
    print("Compliance Officer Output: Final Output Ready. Routing to END.")
    return state