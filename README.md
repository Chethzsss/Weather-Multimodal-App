# 🌦️ Weather Multimodal App

A simple Streamlit app that uses Google's Gemini model to analyze images and answer weather-related questions.

## 🚀 Deployment
- Repo is ready for [Streamlit Cloud](https://streamlit.io/cloud).
- API key is stored in **Streamlit Secrets**, not in `.env`.

## 🔑 Secrets
In Streamlit Cloud, go to **App → Settings → Secrets** and add:

```toml
GOOGLE_API_KEY="your-google-api-key"
