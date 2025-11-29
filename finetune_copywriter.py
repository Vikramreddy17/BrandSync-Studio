# finetune_copywriter.py
import torch
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# Define the formatting function for the dataset
def format_instruction_examples(examples):
    # Transforms the dataset into the standard Llama instruction format
    prompts = []
    for tone, caption in zip(examples['tone_label'], examples['caption']):
        # Using a simple instruction template for brand voice alignment
        text = f"### Instruction:\nWrite a social media caption with a '{tone}' tone.\n\n### Response:\n{caption}"
        prompts.append(text)
    return {"text": prompts}

# --- 1. Load Model and Tokenizer ---
def run_finetuning():
    max_seq_length = 2048 
    
    # Load Llama 3.1 8B, load_in_4bit=True enables QLoRA
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "meta-llama/Llama-3.1-8B",
        max_seq_length = max_seq_length,
        dtype = None, 
        load_in_4bit = True,
    )

    # --- 2. Configure QLoRA ---
    model = FastLanguageModel.get_peft_model(
        model,
        r = 16,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha = 32,
        lora_dropout = 0.05,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
        random_state = 3407,
    )

    # --- 3. Load and Process Dataset ---
    dataset = load_dataset("declare-lab/BrandVoice", split="train")

    # Apply the instruction formatting
    dataset = dataset.map(
        format_instruction_examples, 
        batched = True, 
        remove_columns=dataset.column_names
    )

    # --- 4. Setup Trainer ---
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_workers = 4,
        packing = True,
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 100,  # 100 steps as per plan
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 10,
            output_dir = "models/copywriter-finetuned",
            optim = "adamw_8bit",
            seed = 3407,
        ),
    )

    # --- 5. Train and Save ---
    print("Starting Fine-Tuning (100 steps)...")
    trainer.train()

    # Save the QLoRA adapters
    model.save_pretrained_merged("models/copywriter-finetuned", tokenizer, save_method = "json")
    print("Fine-tuning complete. Model saved to models/copywriter-finetuned.")

if __name__ == "__main__":
    run_finetuning()