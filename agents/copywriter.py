# agents/copywriter.py
from ollama import Client
import json

# Minimal class definition needed for function signature (avoids circular import)
class AgentState: pass 

client = Client(host='http://localhost:11434')

def copywriter(state: AgentState) -> AgentState:
    """Writes content using Ollama and prompt engineering (mocking fine-tuned brand voice)."""
    strategy = state["strategy"]
    feedback = state.get("brand_feedback", "None")
    rev_count = state.get("revision_count", 0)

    if "REJECT" in feedback:
        state["revision_count"] = rev_count + 1
        rev_count += 1

    prompt = f"""
    You are a viral social media copywriter specializing in brand consistency.
    STRATEGY: {strategy}
    PREVIOUS FEEDBACK: {feedback}

    Your goal is to write a single, attention-grabbing social media caption (max 3 sentences).
    Ensure the copy strictly follows the TONE defined in the strategy.
    """
    
    try:
        response = client.generate(
            model='llama3.1:8b', 
            prompt=prompt,
            stream=False,
            options={'temperature': 0.8 if rev_count == 0 else 0.4}
        )
        new_copy = response['response'].strip()
    except Exception as e:
        print(f"Ollama Error in Copywriter: {e}. Using fallback.")
        new_copy = f"ERROR: Ollama failed. Fallback Copy (Rev {rev_count}). Consistency is key, even when the AI fails!"

    # Mock the behavior for the demo to force rejection/pass
    if rev_count == 0:
        new_copy = "BrandSync Studio is the new standard for AI content creation. Our platform ensures total brand consistency across all channels. Sign up today!"
    elif rev_count == 1:
        new_copy = "GUARANTEED PASS: The revised copy is highly engaging and maintains the playful tone. Rework is history! #BrandSyncSuccess"


    state["copy"] = new_copy
    print(f"Copywriter Output (Rev {rev_count}): {state['copy'][:50]}...")
    return state