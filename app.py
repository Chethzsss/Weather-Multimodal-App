import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure API key from Streamlit Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Weather Multimodal App", layout="wide")

st.title("🌦️ Weather Multimodal Q&A")
st.write("Upload an image and optionally ask a weather-related question.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
user_prompt = st.text_input("Ask something about the image (optional):")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    model = genai.GenerativeModel("gemini-1.5-flash")

    # Send image + optional text prompt
    response = model.generate_content(
        [user_prompt, image] if user_prompt else [image]
    )

    st.subheader("🔍 Answer")
    st.write(response.text)
