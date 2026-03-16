import argparse
from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- Accept model path as a command-line argument ---
parser = argparse.ArgumentParser(description="Chat with a local Coryn model via API.")
parser.add_argument(
    "model_path",
    type=str,
    help="Path to the model directory or checkpoint, e.g. ./coryn_130m"
)
args = parser.parse_args()

# Load model and tokenizer
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading model from: {args.model_path}")
print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained(args.model_path)
tokenizer.pad_token_id = tokenizer.eos_token_id

model = AutoModelForCausalLM.from_pretrained(
    args.model_path,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)
model.eval()

print("Model ready for API.")

SYSTEM_PROMPT = "<|system|>\nYou are a helpful, friendly, and honest assistant.\n"

# Initialize Flask app
app = Flask(__name__)
history = SYSTEM_PROMPT

@app.route('/chat/completions', methods=['POST'])
def chat_endpoint():
    global history
    data = request.get_json()
    user_input = data.get('message', '').strip()
    if not user_input:
        return jsonify({'reply': ''})

    # Append user turn to history
    history += f"<|user|>\n{user_input}\n<|assistant|>\n"

    inputs = tokenizer(history, return_tensors="pt").to(device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

    new_tokens = output_ids[0][inputs["input_ids"].shape[-1]:]
    response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    # Append assistant reply to history
    history += f"{response}\n"

    # Trim history if it grows too long
    if len(history) > 2000:
        history = SYSTEM_PROMPT + history[-(2000 - len(SYSTEM_PROMPT)):] 

    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)