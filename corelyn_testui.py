import gradio as gr
import requests

API_URL = "http://192.168.0.136:5000/chat/completions" # Replace link here

# Function to send user messages to the API and get responses
def chat_with_api(user_message, chat_history):
    chat_history = chat_history or []

    # Convert previous chat to proper format if needed
    formatted_history = []
    for item in chat_history:
        if isinstance(item, dict) and 'role' in item and 'content' in item:
            formatted_history.append(item)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            formatted_history.append({'role': 'user' if item[0] == 'User' else 'assistant', 'content': str(item[1])})

    # Append current user message
    formatted_history.append({'role': 'user', 'content': str(user_message)})

    try:
        response = requests.post(API_URL, json={"message": user_message}, timeout=10)
        response.raise_for_status()
        data = response.json()
        bot_message = str(data.get("reply", "Sorry, no reply from server."))
    except Exception as e:
        bot_message = f"Error: {str(e)}"

    # Append bot message
    formatted_history.append({'role': 'assistant', 'content': bot_message})

    # Convert back to list of dicts for Gradio Chatbot
    return "", formatted_history

# Custom CSS to remove branding and style the app, center top icon

# Build Gradio interface
with gr.Blocks() as demo:
    with gr.Column():
        gr.Image(value="./images/mlm_logo.png", elem_id="top_icon", show_label=False, interactive=False, type="filepath")
    chatbot = gr.Chatbot(elem_id="chatbot")
    msg = gr.Textbox(placeholder="Type your message here...", label="")
    clear = gr.Button("Clear")

    msg.submit(chat_with_api, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: ("", []), None, [msg, chatbot])

if __name__ == "__main__":
    demo.launch(share=False)