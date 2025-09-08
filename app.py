import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Multimodal Weather Q&A", page_icon="🌤️")

st.title("🌤️ Multimodal Weather Q&A (Gemini)")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores conversation
if "image" not in st.session_state:
    st.session_state.image = None   # Stores uploaded image

# --- Config ---
MAX_FILE_SIZE_MB = 5
SYSTEM_PROMPT = "You are a helpful weather assistant. Analyze the uploaded image and answer questions clearly."


# --- Sidebar controls ---
st.sidebar.header("⚙️ Model Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
top_k = st.sidebar.slider("Top-K Sampling", 1, 50, 40, 1)
show_prompt = st.sidebar.checkbox("Show system prompt", value=False)


# --- File upload ---
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"❌ File too large: {file_size_mb:.2f} MB. Please upload under {MAX_FILE_SIZE_MB} MB.")
        st.session_state.image = None
    else:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.session_state.image = image
            st.session_state.messages = []  # Reset history on new image
        except UnidentifiedImageError:
            st.error("❌ Invalid image file. Please upload a valid JPG or PNG.")
            st.session_state.image = None


# --- User input ---
user_question = st.text_input("Ask a question about the image", placeholder="e.g., Does it look cloudy?")


# --- Ask button ---
if st.button("Ask"):
    if st.session_state.image is None:
        st.warning("⚠️ Please upload a valid image first.")
    elif not user_question.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        try:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config={
                    "temperature": temperature,
                    "top_k": top_k,
                },
            )

            # Add question to history
            st.session_state.messages.append({"role": "user", "content": user_question})

            with st.spinner("Analyzing..."):
                start_time = time.time()
                response = model.generate_content(
                    [SYSTEM_PROMPT] + [m["content"] for m in st.session_state.messages] + [st.session_state.image]
                )
                end_time = time.time()

            answer = response.text
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # Show response time
            st.success(f"✅ Response generated in {end_time - start_time:.2f} seconds.")

        except Exception as e:
            st.error(f"❌ API error: {str(e)}")


# --- Show conversation history ---
if st.session_state.messages:
    st.subheader("Conversation")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 Gemini:** {msg['content']}")

# --- Show system prompt ---
if show_prompt:
    st.sidebar.subheader("📜 Current System Prompt")
    st.sidebar.code(SYSTEM_PROMPT, language="markdown")
