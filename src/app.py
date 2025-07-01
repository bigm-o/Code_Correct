import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io

# --- Gemini API Configuration ---
gemini_api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="🤖 Code Correct AI Chatbot", layout="centered")

page_bg_img = f"""
<style>
.st-emotion-cache-bm2z3a {{
    background-image: url("image.jpg"):
    background-size: cover;
}}
.st-emotion-cache-h4xjwg {{
    background-color: gba(0, 0, 0, 0);
}}
.st-emotion-cache-qcpnpn {{  
    background-color: gba(0, 0, 0, 0.6);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """,
    unsafe_allow_html=True
)

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
        <br>
        <br><br>
        <br><br>
        <br>
        I'm here fix bugs, troubleshoot software issues and help you write cleaner more efficient code to keep your PC running smoothly.
        
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
        {"role": "user", "parts": [{"text": system_instruction_prompt}]},
        {"role": "assistant", "parts": [{"text": "Hello! How can I help you with your code today?"}]}
    ]

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        for part in message["parts"]:
            if "text" in part:
                st.markdown(part["text"])
            elif "image" in part:
                # This 'image' part already contains the PIL Image object
                st.image(part["image"], caption="Uploaded Image", use_container_width=True)

# --- Chat Input with File Acceptance ---
prompt_input = st.chat_input(
    "Ask me about your code or upload an image for analysis...",
    accept_file=True, # This enables file uploads directly in the chat input
    file_type=["png", "jpg", "jpeg"] # Specify allowed file types
)

if prompt_input:
    user_text = prompt_input.text
    uploaded_files = prompt_input.files # This is a list of UploadedFile objects

    # Prepare the parts for the user's message
    user_message_parts = []
    
    # Add the text prompt if available
    if user_text:
        user_message_parts.append({"text": user_text})

    # If images were uploaded, process and add them to the message parts
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                image_data = uploaded_file.read() # Read the file data ONCE
                pil_image = Image.open(io.BytesIO(image_data))
                user_message_parts.append({"image": pil_image}) # Store PIL Image object
            except Exception as e:
                st.error(f"Error processing image {uploaded_file.name}: {e}. This image will not be sent.")
                # Continue processing other files if multiple were uploaded
                continue 

    # Store and display the current user prompt.
    st.session_state.messages.append({"role": "user", "parts": user_message_parts})
    
    with st.chat_message("user"):
        for part in user_message_parts: # Iterate through the parts we just created
            if "text" in part:
                st.markdown(part["text"])
            elif "image" in part:
                # Use the PIL Image object directly from the stored parts
                st.image(part["image"], caption="Your Uploaded Image", use_container_width=True)

    # Prepare messages for Gemini API from the session state.
    gemini_messages_for_api = []
    for msg in st.session_state.messages:
        role_for_gemini = "user" if msg["role"] == "user" else "model"
        
        parts_for_gemini = []
        for part in msg["parts"]:
            if "text" in part:
                parts_for_gemini.append({"text": str(part["text"])})
            elif "image" in part:
                parts_for_gemini.append(part["image"]) # Directly pass the PIL Image object
        
        gemini_messages_for_api.append({"role": role_for_gemini, "parts": parts_for_gemini})

    # Generate a response using the Gemini API.
    try:
        stream = model.generate_content(
            gemini_messages_for_api,
            stream=True,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024
            )
        )

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response_content = ""
            for chunk in stream:
                if chunk.text:
                    full_response_content += chunk.text
                    message_placeholder.markdown(full_response_content + "▌")
            message_placeholder.markdown(full_response_content)
            
        st.session_state.messages.append({"role": "assistant", "parts": [{"text": full_response_content}]})
        

    except Exception as e:
        st.error(f"An error occurred while generating response: {e}")
        st.warning("Please try again. If the issue persists, verify your API key or the model's availability.") 