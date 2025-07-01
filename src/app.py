import streamlit as st
import google.generativeai as genai
import os

# --- Gemini API Configuration ---
gemini_api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="🤖 Code Correct AI Chatbot", layout="centered")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("image.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """,
    unsafe_allow_html=True
)

# st.title("👨‍💻 Welcome to Code Correct 🤓")
# st.write(
#     "Your dedicated AI assistant for all things code! "
#     "Whether you need to fix bugs, understand complex concepts, or troubleshoot software issues, "
#     "I'm here to help you write cleaner, more efficient code and keep your PC running smoothly."
# )

st.markdown(
    """
    <h1 style="display: flex; align-items: center; justify-content: center; gap: 10px; text-align: center;">
        <i class="fas fa-robot" style="color: #FFD700;"></i> CODE CORRECT  
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center; font-size: 1.5rem;">
        Your dedicated AI assistant for all things code! 
        <br><br>Whether you need to fix bugs, understand complex concepts, or troubleshoot software issues, 
        I'm here to help you write cleaner, more efficient code and keep your PC running smoothly.
    </div>
    """,
    unsafe_allow_html=True
)


# Check if API key is available from secrets/environment variables
if not gemini_api_key:
    st.error("Gemini API Key not found. Please ensure it's set in your `.streamlit/secrets.toml` file or as an environment variable.")
    st.stop()

try:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}. Please verify your API key's validity.")
    st.stop()

# --- Read the prompt from prompt.txt ---
# Ensure prompt.txt is in the same directory as app.py
try:
    with open("prompt.txt", "r") as f:
        system_instruction_prompt = f.read().strip()
except FileNotFoundError:
    st.error("Error: 'prompt.txt' not found. Please make sure the prompt file is in the same directory as 'app.py'.")
    st.stop()
except Exception as e:
    st.error(f"Error reading 'prompt.txt': {e}")
    st.stop()

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Initial 'user' message as system instruction for Gemini, loaded from the file
        {"role": "user", "content": system_instruction_prompt},
        # Initial 'assistant' (model) response to complete the first turn
        {"role": "assistant", "content": "Hello! How can I help you with your code today?"}
    ]

# Display the existing chat messages via `st.chat_message`.
# We skip displaying the first two messages (system instruction and initial greeting)
# as they are internal to the model's context and not meant for user display.
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message.
if prompt := st.chat_input("Ask me about your code..."):

    # Store and display the current user prompt.
    # Ensure the prompt content is explicitly converted to a string.
    st.session_state.messages.append({"role": "user", "content": str(prompt)})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare messages for Gemini API from the session state.
    # Convert Streamlit's message format to Gemini's expected format.
    gemini_messages_for_api = []
    for msg in st.session_state.messages:
        # Ensure role is 'user' or 'model' for Gemini API
        role_for_gemini = "user" if msg["role"] == "user" else "model"
        # Ensure the content is explicitly converted to a string before being part of the API request.
        gemini_messages_for_api.append({"role": role_for_gemini, "parts": [{"text": str(msg["content"])}]})

    # Generate a response using the Gemini API.
    try:
        # Get the stream from Gemini
        stream = model.generate_content(
            gemini_messages_for_api, # Pass the entire history
            stream=True,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024
            )
        )

        # Stream the response to the chat using `st.write_stream`, then store it.
        # IMPORTANT CHANGE: Extract only the 'text' from each chunk of the stream.
        with st.chat_message("assistant"):
            # Create a generator that yields only the text content from each chunk
            text_stream = (chunk.text for chunk in stream)
            response_content = st.write_stream(text_stream)
            
        # Store the full response content in session state, ensuring it's a plain string.
        st.session_state.messages.append({"role": "assistant", "content": str(response_content)})

    except Exception as e:
        st.error(f"An error occurred while generating response: {e}")
        st.warning("Please try again. If the issue persists, verify your API key or the model's availability.")

