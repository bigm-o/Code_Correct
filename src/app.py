import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io
import base64 
import random

# --- Gemini API Configuration ---
gemini_api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="🤖 Code Correct AI Chatbot", layout="centered")

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """,
    unsafe_allow_html=True
)

# --- Image Encoding Function ---
def get_base64_image(image_path):
    try:
        # Determine MIME type based on file extension
        # You might need to adjust this if you use other image types
        if image_path.lower().endswith(('.png')):
            mime_type = "image/png"
        elif image_path.lower().endswith(('.jpg', '.jpeg')):
            mime_type = "image/jpeg"
        elif image_path.lower().endswith(('.gif')):
            mime_type = "image/gif"
        else:
            mime_type = "image/jpeg"
            st.warning(f"Unknown image type for {image_path}. Defaulting to image/jpeg.")

        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
        return f"data:{mime_type};base64,{encoded_string}"
    except FileNotFoundError:
        st.error(f"Background image not found at: {image_path}. Please ensure the file exists.")
        return ""
    except Exception as e:
        st.error(f"Error encoding background image: {e}")
        return ""

# --- Specify your local background image path ---
image_number = random.randint(1, 6)
BACKGROUND_IMAGE_PATH = f"images/image{image_number}.jpg"
encoded_background_image = get_base64_image(BACKGROUND_IMAGE_PATH)

# --- Custom CSS for Styling ---
st.markdown(f"""
<style>
    /* Google Fonts Import - MUST be at the top of the <style> block */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;700&display=swap');

    /* Overall App Background and Font */
    html, body {{
        font-family: 'Poppins', sans-serif;
        background-color: #f0f2f6; /* Fallback background color */
    }}

    /* Target Streamlit's main container for background image */
    [data-testid="stApp"] {{
        background-image: url("{encoded_background_image}"); /* Using Base64 encoded image */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #e0e0e0; 
    }}

    [data-testid="stApp"] {{
        background-image: url("{encoded_background_image}"); /* Using Base64 encoded image */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #e0e0e0; 
    }}

    .stAppViewContainer {{
        position: fixed;
        inset: 0;
        background-color: rgba(0, 0, 0, 0.82);
    }}


    /* NEW: Target the chat input's outer container to make its background transparent */
    [data-testid="stBottom"] {{
        background-color: transparent !important;
    }}

    [data-testid="stMarkdownContainer"] {{
        color: white;
    }}

    [data-testid="stChatMessageContent"] {{
        padding: 1.5rem
    }}

    [data-testid="stMainBlockContainer"] {{
        padding: 4rem 1rem 1rem;
    }}

    [data-testid="stChatMessageAvatarUser"] svg {{
        color: rgb(14, 17, 23);
    }}

    [data-testid="stChatMessageAvatarAssistant"] svg {{
        color: rgb(14, 17, 23);
    }}

    [data-testid="stCaptionContainer"] {{
        color: rgb(250, 250, 250);
    }}

    [data-testid="stChatInputDeleteBtn"] {{
        color: #e0e0e0;
    }}

    [data-testid="stElementToolbarButtonContainer"] {{
        background-color: rgb(19, 23, 32);
    }}

    [data-testid="stElementToolbarButtonIcon"] {{
        color: white;
    }}

    .st-emotion-cache-yg4ae2 {{
        color: rgb(250, 250, 250, 0.6);
    }}

    .st-emotion-cache-hzygls {{
        background-color: transparent !important;
    }}

    .st-emotion-cache-128upt6 {{
        background-color: transparent !important;
    }}

    .st-emotion-cache-uzemrq {{
        background: rgb(26, 28, 36);
        color: rgb(61, 213, 109);
    }}

    .st-emotion-cache-14drx84 {{
        background: rgb(26, 28, 36);
        color: white;
    }}

    .st-emotion-cache-1o07ofn {{
        color: rgba(250, 250, 250, 0.6);
    }}

    .stChatMessage {{
        background-color: rgba(38, 39, 48, 0.5);
    }}

    .stChatInputFileName {{
        color: white;
    }}

    .st-emotion-cache-1i3z4bt {{
        color: white;
    }}

    /* Adjust main content block padding and background for readability */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-left: auto;
        margin-right: auto;
        max-width: 1200px; /* Limit width for better readability */
    }}

    /* Chat message styling */
    .st-chat-message-container {{
        background-color: rgba(255, 255, 255, 0.95); /* Slightly transparent white for chat messages */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}

    .st-chat-message-container.st-chat-message-user {{
        background-color: rgba(230, 247, 255, 0.95); /* Light blue for user messages */
        border-left: 5px solid #1890ff;
    }}

    .st-chat-message-container.st-chat-message-assistant {{
        background-color: rgba(240, 240, 240, 0.95); /* Light gray for assistant messages */
        border-right: 5px solid #4CAF50;
    }}

    /* Input field styling (st.text_input, st.text_area, st.chat_input) */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .st-emotion-cache-1c7y2vl > div > input {{ /* Specific selector for st.chat_input */
        border-radius: 8px;
        border: 1px solid #007bff; /* Blue border */
        padding: 12px;
        font-size: 16px;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
        background-color: #ffffff; /* White background for inputs */
        color: #333; /* Dark text color */
    }}

    /* Button styling */
    div.stButton > button {{
        background-color: #007bff; /* Blue */
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }}
    div.stButton > button:hover {{
        background-color: #0056b3; /* Darker blue on hover */
        transform: translateY(-2px);
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: #2c3e50; /* Darker text for headers */
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
    }}

    .st-chat-message-container pre {{
        background-color: #2d2d2d; /* Dark background for code */
        color: #f8f8f2; /* Light text for code */
        padding: 15px;
        border-radius: 8px;
        overflow-x: auto; /* Allow horizontal scrolling for long code lines */
        font-family: 'Roboto Mono', monospace;
        font-size: 0.9rem;
        white-space: pre-wrap; /* Ensure code wraps */
        word-break: break-all; /* Break long words if necessary */
    }}
    
    .stSpinner > div {{
        color: #007bff !important; /* Blue spinner */
    }}

    .simple-repo-button {{
        background-color: #282c34;
        color: white;
        border: 2px solid #61dafb;
        padding: 12px 25px;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }}

   .simple-repo-button:hover {{
        background-color: #61dafb !important; 
        color: #282c34 !important; 
        transform: translateY(-2px); 
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4); 
    }}

    /* Hide element on small mobile devices */
    @media (max-width: 767px) {{
        .hide-on-mobile {{
            display: none !important;
        }}
    }}

    /* Example: Show element only on mobile */
    @media (min-width: 768px) {{
        .show-only-mobile {{
            display: none !important;
        }}
    }}

</style>
""", unsafe_allow_html=True)




st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; text-align: center; font-size: 3rem;">
        <i class="fas fa-robot" style="color: #ffffff;"></i>
    </div>
    <br>
    <div style="display: flex; align-items: center; justify-content: center; text-align: center; font-size: 3rem;">
        <strong>CODE CORRECT</strong>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center; font-size: 1.5rem;">
        Your dedicated AI assistant for all things code
        <br>
        <div style="text-align: center; margin-top: 30px; margin-bottom: 30px;">
            <a href="https://github.com/bigm-o/Code_Correct.git" target="_blank" class="simple-repo-button">
                <i class="fab fa-github"></i> View on GitHub
            </a>
        </div>
        <br>
        <span class="hide-on-mobile">
        I'm to here fix bugs, troubleshoot software issues and help you write cleaner, more efficient codes to keep your PC and projects running smoothly.
        </span>
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
    with open("src/prompt.txt", "r") as f:
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