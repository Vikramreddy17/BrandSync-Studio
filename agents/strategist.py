# agents/strategist.py
from ollama import Client
import json

# Minimal class definition needed for function signature (avoids circular import)
class AgentState: pass 

client = Client(host='http://localhost:11434')

def strategist(state: AgentState) -> AgentState:
    """Takes user brief, defines tone, keywords, and goals using Llama 3.1 8B via Ollama."""
    brief = state["brief"]
    
    prompt = f"""
    Analyze the following creative brief. Output your response as a single, valid JSON object with the keys: "tone" (e.g., Playful, Energetic), "keywords" (list of 3-5), and "goal" (short phrase).

    BRIEF: {brief}
    """
    
    try:
        response = client.generate(
            model='llama3.1:8b', 
            prompt=prompt,
            stream=False,
            options={'temperature': 0.1}
        )
        json_output = json.loads(response['response'].strip().strip('```json').strip('```').strip())
        
        state["strategy"] = (
            f"Tone: {json_output.get('tone', 'Professional')}; "
            f"Keywords: {', '.join(json_output.get('keywords', ['AI', 'Consistency']))}; "
            f"Goal: {json_output.get('goal', 'Engagement')}"
        )
    except Exception as e:
        # NOTE: This fallback ensures the demo runs even if Ollama is not outputting perfect JSON
        print(f"Ollama/JSON Error in Strategist: {e}. Using mock data.")
        state["strategy"] = "Tone: Playful & Direct; Keywords: Autonomous AI, Consistency; Goal: Engagement"
        
    state["revision_count"] = state.get("revision_count", 0)
    print(f"Strategist Output: {state['strategy']}")
    return state