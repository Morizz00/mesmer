from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


base_model = "microsoft/phi-2" 
adapter_path = "./mesmer_finetune/checkpoint-186"
output_dir = "./finetuned_mesmer"

print(" Loading base model...")
model = AutoModelForCausalLM.from_pretrained(base_model)
tokenizer = AutoTokenizer.from_pretrained(base_model)

print("Loading LoRA adapter...")
model = PeftModel.from_pretrained(model, adapter_path)

print(" Merging adapter weights...")
model = model.merge_and_unload()

print("Saving full model...")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(" Full model saved at:", output_dir)