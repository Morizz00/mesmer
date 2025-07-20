import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

print(" Loading fine-tuned Mesmer model...")
model_path = "./finetuned_mesmer"


tokenizer = AutoTokenizer.from_pretrained(model_path)


model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,   
).to("cuda")                    


generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0  # using GPU
)

def query_llm(conversation_history, mode="homie"):
    print(" Generating response locally using Phi-2 fine-tuned model.")

    
    user_text = conversation_history[-1]["content"]
    prompt = f"### Instruction:\n{user_text}\n### Response:\n"


    output = generator(
        prompt,
        max_new_tokens=200,       
        temperature=0.7,          
        top_p=0.9,               
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    reply = output[0]["generated_text"].split("### Response:")[-1].strip()
    return reply