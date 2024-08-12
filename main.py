import requests  # For making HTTP requests to the API
import json  # For handling JSON data
import gradio as gr  # For creating the user interface

# URL of the API endpoint that generates responses
URL = "http://localhost:11434/api/generate"
# Headers to be used for the HTTP request
HEADERS = {'Content-Type': 'application/json'}
# List to store the conversation history
conversation_history = []


def generate_response(prompt):
    """
    Function to send a prompt to the API and get a response.

    Args:
        prompt (str): The user's input prompt.

    Returns:
        str: The formatted chat history including the new response.
    """
    # Append the user's prompt to the conversation history
    conversation_history.append(("User", prompt))

    # Create a full prompt by joining the conversation history
    full_prompt = "\n".join([f"{sender}: {msg}" for sender, msg in conversation_history])

    # Data to be sent to the API
    data = {
        "model": "llama3",  # Specify the model to use
        "stream": False,  # Whether to stream the response (set to False here)
        "prompt": full_prompt,  # The full prompt including conversation history
    }

    # Make a POST request to the API
    response = requests.post(URL, headers=HEADERS, json=data)

    # Check if the response was successful
    if response.ok:
        # Extract the response text from the JSON response
        response_text = response.json().get("response", "Error: No response")
    else:
        # Handle errors by extracting status code and error message
        response_text = f"Error: {response.status_code}, {response.text}"

    # Append the API's response to the conversation history
    conversation_history.append(("Bot", response_text))

    # Return the formatted chat messages
    return format_chat_messages(conversation_history)


def clear_history():
    """
    Function to clear the conversation history.

    Returns:
        list: An empty list indicating that history has been cleared.
    """
    # Clear the conversation history
    conversation_history.clear()
    return []


def format_chat_messages(messages):
    """
    Function to format chat messages for display.

    Args:
        messages (list): List of tuples where each tuple is (sender, message).

    Returns:
        list: Formatted messages for the chat interface.
    """
    # Format each message for HTML display
    return [(None, f"<div><b>{sender}:</b> {msg}</div>") for sender, msg in messages]


# Create the Gradio interface
with gr.Blocks() as iface:
    # Create a chatbot interface element
    chatbot = gr.Chatbot(label="Chat with AI", height=500)
    with gr.Row():
        with gr.Column(scale=0.85):
            # Textbox for user input
            user_input = gr.Textbox(show_label=False, placeholder="Enter your prompt here...")
        with gr.Column(scale=0.15, min_width=0):
            # Button to submit the user's prompt
            submit_btn = gr.Button("Send")
    # Button to clear the chat history
    clear_btn = gr.Button("Clear History")

    # Define actions for buttons
    submit_btn.click(lambda prompt: generate_response(prompt), inputs=user_input, outputs=chatbot)
    clear_btn.click(clear_history, outputs=chatbot)

# Launch the Gradio interface
iface.launch()
