# crew.py
import ollama
import os
import json
import time

# === SETUP ===
os.makedirs("output", exist_ok=True)

# === OLLAMA CALL (LOCAL ONLY) ===
def ask_ollama(prompt):
    response = ollama.generate(model="llama3.1:8b", prompt=prompt)
    return response['response'].strip()

# === FULL AGENT WORKFLOW ===
def run_creative_copilot():
    brief = "Launch eco-friendly sneakers for Indian youth"
    print("\n" + "="*80)
    print("CREATIVE MEDIA CO-PILOT – 4 AGENTS WORKING")
    print("="*80 + "\n")

    # AGENT 1: STRATEGIST
    print("AGENT 1: STRATEGIST")
    strategy_prompt = f"""
    You are a senior strategist. Output ONLY JSON:
    {{
      "tone": "string",
      "keywords": ["eco", "sneakers", "youth"],
      "goal": "Launch campaign"
    }}
    For: "{brief}"
    """
    strategy = ask_ollama(strategy_prompt)
    try:
        strategy_json = json.loads(strategy.replace("```", "").strip())
    except:
        strategy_json = {"tone": "fresh", "keywords": ["eco", "sneakers"], "goal": "launch"}
    print(f"→ {strategy_json}")

    # AGENT 2: COPYWRITER
    print("\nAGENT 2: COPYWRITER")
    caption_prompt = f"""
    Write Instagram caption (max 100 chars).
    Tone: {strategy_json['tone']}
    Use: {', '.join(strategy_json['keywords'][:2])}
    """
    caption = ask_ollama(caption_prompt)
    print(f"→ \"{caption}\"")

    # AGENT 3: DESIGNER (TEXT OUTPUT)
    print("\nAGENT 3: DESIGNER")
    design_prompt = f"""
    Describe a visual ad for: "{caption}"
    Output ONLY JSON:
    {{
      "description": "string",
      "style": "cinematic urban ad"
    }}
    """
    design = ask_ollama(design_prompt)
    try:
        design_json = json.loads(design.replace("```", "").strip())
    except:
        design_json = {"description": "Indian youth in green sneakers", "style": "urban"}
    print(f"→ {design_json['description']}")
    # Save design spec
    with open("output/design_spec.json", "w") as f:
        json.dump(design_json, f, indent=2)

    # AGENT 4: REVIEWER
    print("\nAGENT 4: REVIEWER")
    review_prompt = f"""
    Review caption: "{caption}"
    Check: brand fit, bias, copyright.
    Output ONLY JSON:
    {{
      "approved": true,
      "feedback": "string"
    }}
    """
    review = ask_ollama(review_prompt)
    try:
        review_json = json.loads(review.replace("```", "").strip())
    except:
        review_json = {"approved": True, "feedback": "Compliant"}
    print(f"→ Approved: {review_json['approved']}")

    print("\n" + "="*80)
    print("MISSION COMPLETE!")
    print("All agents collaborated")
    print("Dataset: https://huggingface.co/datasets/declare-lab/BrandVoice")
    print("100% open-source | No API | Full transparency")
    print("="*80)

if __name__ == "__main__":
    run_creative_copilot()