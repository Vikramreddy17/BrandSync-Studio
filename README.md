# BrandSync Studio 🖌️✨

**Autonomous AI Creative Agency** for solo creators & teams, guaranteeing **brand-safe** and **compliant** content in one click.

## 🎯 Features

- **5 Specialized Agents:** Orchestrated team for Strategy, Copywriting, Design, Guardianship, and Compliance.
- **Brand Voice Alignment:** Uses **QLoRA Fine-tuning** on Llama 3.1 for custom tone alignment.
- **Autonomous Validation Loop:** **LangGraph** enforces a two-cycle Brand Guardian review before approval.
- **100% Open-Source Stack:** Built on Llama 3.1, Stable Diffusion, and LangGraph.

## 🛠 Tech Stack

- **LLM**: Llama 3.1 8B (via Ollama or HuggingFace)
- **Framework**: LangGraph (by LangChain)
- **Image Gen**: Stable Diffusion 1.5/XL (via Diffusers)
- **Fine-tuning**: Unsloth + QLoRA on **BrandVoice Dataset**

## 🚀 Setup & Quick Start

1.  **Clone the repository and set up environment (Python 3.11+ is recommended):**
    ```bash
    git clone [https://github.com/YourUsername/BrandSync-Studio.git](https://github.com/YourUsername/BrandSync-Studio.git)
    cd BrandSync-Studio
    python -m venv .venv
    .venv/Scripts/activate # or source .venv/bin/activate on Linux/Mac
    ```

2.  **Install Ollama and pull the model:**
    ```bash
    # Download Ollama server separately
    ollama pull llama3.1:8b
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Fine-tune the Copywriter Agent:**
    ```bash
    python finetune_copywriter.py
    ```
    *This is necessary to create the `models/copywriter-finetuned` directory.*

5.  **Run the Streamlit UI:**
    ```bash
    streamlit run app.py
    ```

---

The code for the multi-agent system demonstrates how to prompt AI agents and customize them for specific marketing tasks, including strategy definition and copywriting. The video, [Prompt Like a Pro: Agentic Marketing Best Practices](https://www.youtube.com/watch?v=3NmvlQ0oqUI), provides context on best practices for agentic marketing architectures.
http://googleusercontent.com/youtube_content/0